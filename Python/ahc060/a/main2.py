import sys
import math
import random
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

# ------------------------------------------------------------------------------
# クラス・関数定義
# ------------------------------------------------------------------------------

class IceCreamSolver:
    """
    AHC 'Ice Cream Collection' 問題を解くためのソルバークラス。
    
    Attributes:
        N, M, K, T: 問題の基本パラメータ
        adj: 隣接リスト
        shop_inventories: 各ショップの在庫集合
        tree_flavors: 各木の現在の味
        target_flavors: 各木の目標の味（戦略的に決定）
        current_ice_cream: 現在持っているアイス文字列
        current_pos: 現在位置
        prev_pos: 直前の位置（Uターン禁止用）
        setup_targets: 戦略的にRに変えるべき頂点の集合
        move_queue: 決定済みの行動予定リスト (パスキャッシュ)。正の値は移動、-1は味変を表す。
        consecutive_fails: 探索失敗が続いた回数
    """

    def __init__(self):
        """初期化と入力受取"""
        try:
            line1 = input().split()
            if not line1: return
            self.N, self.M, self.K, self.T = map(int, line1)

            self.adj = [[] for _ in range(self.N)]
            for _ in range(self.M):
                line = input().split()
                u, v = int(line[0]), int(line[1])
                self.adj[u].append(v)
                self.adj[v].append(u)

            self.coords = []
            for _ in range(self.N):
                line = input().split()
                x, y = int(line[0]), int(line[1])
                self.coords.append((x, y))

        except (EOFError, ValueError):
            return

        # --- 状態初期化 ---
        self.shop_inventories: List[Set[str]] = [set() for _ in range(self.K)]
        
        # 木の初期味はすべて 'W'
        self.tree_flavors: List[Optional[str]] = [None] * self.N
        for i in range(self.K, self.N):
            self.tree_flavors[i] = 'W'

        self.current_ice_cream = ""
        self.current_pos = 0
        self.prev_pos = -1

        # --- 戦略設定 ---
        # 最終的に盤面の約50%を 'R' にすることを目指すが、
        # 実行は「限界が来たら1つずつ」行う。
        self.target_flavors: List[Optional[str]] = [None] * self.N
        self.setup_targets = set()
        
        random.seed(42)
        for i in range(self.K, self.N):
            if random.random() < 0.5:
                self.target_flavors[i] = 'R'
                self.setup_targets.add(i)
            else:
                self.target_flavors[i] = 'W'

        self.target_shop_index = 0
        
        # パスキャッシュ
        # 今回から「移動(正の整数)」だけでなく「味変(-1)」もキューに入れる
        self.move_queue = deque()
        self.consecutive_fails = 0

    def solve(self):
        """メインループ"""
        for t in range(self.T):
            action = -2 # 未定

            # 1. 予定された行動（パスキャッシュ）がある場合、それを実行
            if self.move_queue:
                action = self.move_queue.popleft()
            
            # 2. 予定がない場合、どうするか考える
            else:
                # 失敗（＝良いルートが見つからない状態）が続いている場合
                # 「今の環境ではもう限界」と判断し、ストロベリーを1つ追加しに行く
                if self.consecutive_fails > self.K:
                    
                    # 味変の旅を計画する
                    if self.plan_expand_move():
                        # 計画成功なら、その最初の一歩を実行
                        if self.move_queue:
                            action = self.move_queue.popleft()
                        else:
                            # move_queueが空なら、現在地で即味変(-1)ということ
                            action = -1
                    else:
                        # 変える場所がもうない等の場合、仕方なく単純移動
                        action = self.get_simple_move_to_target(self.target_shop_index)
                
                else:
                    # まだ限界ではない（はず）。未取得パターンを探す
                    path = self.bfs_find_path(self.target_shop_index)
                    
                    if path:
                        # 見つかった！
                        self.consecutive_fails = 0
                        self.move_queue.extend(path)
                        action = self.move_queue.popleft()
                    else:
                        # 見つからなかった...
                        self.consecutive_fails += 1
                        # とりあえずターゲットに1歩近づく（単純移動）
                        action = self.get_simple_move_to_target(self.target_shop_index)

            # --- 実行と出力 ---
            if action == -1:
                # 行動2: 味変
                print("-1")
                # 実際に味を変える
                if self.is_tree(self.current_pos):
                    self.tree_flavors[self.current_pos] = 'R'
                # 味変は移動ではないので prev_pos は更新しない
                
                # 味変直後は環境が変わるので、失敗カウントをリセットして再探索させる
                self.consecutive_fails = 0
                
            else:
                # 行動1: 移動
                print(f"{action}")
                self.execute_move(action)
            
            sys.stdout.flush()

    def plan_expand_move(self) -> bool:
        """
        「限界が来た」時に呼ばれる。
        現在 'W' だが戦略的に 'R' にしたい木のうち、最も近いものを探す。
        見つかったら、そこへの移動パスと「到着後の味変アクション(-1)」を move_queue に積み、Trueを返す。
        """
        # 候補: 「Rにする予定」かつ「今まだW」の木
        candidates = set([v for v in self.setup_targets if self.tree_flavors[v] == 'W'])
        
        if not candidates:
            return False

        # もし今いる場所が候補地なら、即味変
        if self.current_pos in candidates:
            self.move_queue.append(-1)
            return True

        # BFSで最寄りの候補地を探す
        queue = deque([(self.current_pos, [])])
        visited = {self.current_pos}
        
        # 初手
        for neighbor in self.adj[self.current_pos]:
            if neighbor == self.prev_pos: continue
            
            # いきなり候補地に隣接していたら
            if neighbor in candidates:
                self.move_queue.append(neighbor) # 移動
                self.move_queue.append(-1)       # 味変
                return True

            queue.append((neighbor, [neighbor]))
            visited.add(neighbor)

        # BFSループ
        while queue:
            curr, path = queue.popleft()
            
            # あまり遠くに行き過ぎても効率が悪いので打ち切る（任意）
            if len(path) > 20: 
                break

            for neighbor in self.adj[curr]:
                if neighbor not in visited:
                    if neighbor in candidates:
                        # 発見！
                        # path + [neighbor] を移動キューに追加
                        self.move_queue.extend(path)
                        self.move_queue.append(neighbor)
                        self.move_queue.append(-1) # 最後に味変
                        return True
                    
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return False

    def get_min_distance(self, target_shop: int) -> int:
        """ターゲットショップまでの単純な最短距離（ステップ数）"""
        queue = deque([(self.current_pos, 0)])
        visited = {self.current_pos}
        
        while queue:
            curr, dist = queue.popleft()
            if curr == target_shop: return dist
            
            for neighbor in self.adj[curr]:
                if dist == 0 and neighbor == self.prev_pos: continue
                if self.is_shop(neighbor) and neighbor != target_shop: continue
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return 999999

    def bfs_find_path(self, target_shop: int) -> List[int]:
        """
        未所持の文字列を作れるルートを探す。
        制限: 単純最短距離の 1.5倍 まで。
        """
        base_dist = self.get_min_distance(target_shop)
        if base_dist > 5000: return [] # 到達不能
        
        # 1.5倍で打ち切り (天井関数を使って整数化)
        limit_dist = math.ceil(base_dist * 1.5)
        
        queue = deque()
        came_from = {}
        
        initial_state = (self.current_pos, self.current_ice_cream)
        came_from[initial_state] = None
        
        # 初手
        for neighbor in self.adj[self.current_pos]:
            if neighbor == self.prev_pos: continue
            
            next_ice = self.current_ice_cream
            if self.is_tree(neighbor):
                next_ice += self.tree_flavors[neighbor]
            
            if self.is_shop(neighbor) and neighbor != target_shop: continue

            state = (neighbor, next_ice)
            if state not in came_from:
                came_from[state] = initial_state
                queue.append((neighbor, next_ice, 1)) # depth=1
                
                if neighbor == target_shop:
                    if next_ice not in self.shop_inventories[target_shop]:
                        return self.reconstruct_path(came_from, state)

        # BFSループ
        MAX_STEPS = 3000 # 探索回数制限も少し厳しめに
        steps_count = 0
        
        while queue:
            curr_node, curr_ice, depth = queue.popleft()
            steps_count += 1
            if steps_count > MAX_STEPS: break

            if depth >= limit_dist: continue

            if curr_node == target_shop:
                if curr_ice not in self.shop_inventories[target_shop]:
                    return self.reconstruct_path(came_from, (curr_node, curr_ice))
                continue

            parent_state = came_from.get((curr_node, curr_ice))
            prev_node_in_path = parent_state[0] if parent_state else self.prev_pos

            for neighbor in self.adj[curr_node]:
                if neighbor == prev_node_in_path: continue

                next_ice = curr_ice
                if self.is_tree(neighbor):
                    next_ice += self.tree_flavors[neighbor]
                
                if self.is_shop(neighbor):
                    if neighbor != target_shop: continue
                
                new_state = (neighbor, next_ice)
                new_depth = depth + 1

                if new_depth > limit_dist: continue

                if new_state not in came_from:
                    came_from[new_state] = (curr_node, curr_ice)
                    queue.append((neighbor, next_ice, new_depth))
                    
                    if neighbor == target_shop:
                        if next_ice not in self.shop_inventories[target_shop]:
                            return self.reconstruct_path(came_from, new_state)
        
        return []

    def reconstruct_path(self, came_from: Dict, end_state: Tuple) -> List[int]:
        path = []
        curr = end_state
        while curr is not None:
            node, _ = curr
            path.append(node)
            curr = came_from[curr]
        path.pop()
        path.reverse()
        return path

    def get_simple_move_to_target(self, target_shop: int) -> int:
        """単純移動フォールバック"""
        queue = deque([(self.current_pos, [])])
        visited = {self.current_pos}
        
        for neighbor in self.adj[self.current_pos]:
            if neighbor == self.prev_pos: continue
            if self.is_shop(neighbor) and neighbor != target_shop: continue
            if neighbor == target_shop: return neighbor
            queue.append((neighbor, [neighbor]))
            visited.add(neighbor)

        while queue:
            curr, path = queue.popleft()
            for neighbor in self.adj[curr]:
                if neighbor == self.prev_pos and len(path)==0: continue
                if self.is_shop(neighbor) and neighbor != target_shop: continue
                
                if neighbor == target_shop:
                    return path[0]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        for v in self.adj[self.current_pos]:
            if v != self.prev_pos: return v
        return self.adj[self.current_pos][0]

    def execute_move(self, v: int):
        """移動実行と状態更新"""
        self.prev_pos = self.current_pos
        self.current_pos = v

        if self.is_tree(v):
            self.current_ice_cream += self.tree_flavors[v]
        else:
            if self.current_ice_cream not in self.shop_inventories[v]:
                self.shop_inventories[v].add(self.current_ice_cream)
            self.current_ice_cream = ""
            
            if v == self.target_shop_index:
                self.target_shop_index = (self.target_shop_index + 1) % self.K
                # ターゲット到着時はキューをクリア（古い計画を捨てる）
                self.move_queue.clear()

    def is_tree(self, v: int) -> bool:
        return v >= self.K

    def is_shop(self, v: int) -> bool:
        return v < self.K

if __name__ == "__main__":
    solver = IceCreamSolver()
    solver.solve()