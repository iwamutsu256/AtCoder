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
    
    【事前計算・経路キャッシュ型】
    ショップ間の有効な経路を事前に全て列挙して保存し、
    実行時はその中から「現在の状況で最適な経路」を選ぶことで高速化を図る。
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

        # --- 状態変数の初期化 ---
        self.shop_inventories: List[Set[str]] = [set() for _ in range(self.K)]
        
        # 木の初期味はすべて 'W'
        self.tree_flavors: List[Optional[str]] = [None] * self.N
        for i in range(self.K, self.N):
            self.tree_flavors[i] = 'W'

        # 戦略的にRに変える予定の場所（ランダムに半分）
        self.target_flavors: List[Optional[str]] = [None] * self.N
        self.setup_candidates = set()
        random.seed(42)
        for i in range(self.K, self.N):
            if random.random() < 0.5:
                self.target_flavors[i] = 'R'
                self.setup_candidates.add(i)
            else:
                self.target_flavors[i] = 'W'

        self.current_ice_cream = ""
        self.current_pos = 0
        self.prev_pos = -1
        
        # 移動キュー (決定済みのパス)
        self.move_queue = deque()
        
        # 経路キャッシュ
        # key: start_shop_index, value: list of (end_shop_index, path_list)
        self.cached_paths: Dict[int, List[Tuple[int, List[int]]]] = {}
        
        # 事前計算の実行
        self.precompute_all_paths()

    def precompute_all_paths(self):
        """
        ショップ間の有効な経路を事前に列挙・保存する。
        メモリ制限内で、実用的な経路（遠回りしすぎないもの）のみをキャッシュする。
        """
        # 1. 全点対間最短距離 (Warshall-Floyd) - 枝刈りの基準用
        # N=100 なので O(N^3) でも十分高速
        INF = 9999
        dist_matrix = [[INF] * self.N for _ in range(self.N)]
        for i in range(self.N): dist_matrix[i][i] = 0
        for u in range(self.N):
            for v in self.adj[u]:
                dist_matrix[u][v] = 1
        
        for k in range(self.N):
            for i in range(self.N):
                for j in range(self.N):
                    dist_matrix[i][j] = min(dist_matrix[i][j], dist_matrix[i][k] + dist_matrix[k][j])
        
        self.dist_matrix = dist_matrix

        # 2. パス列挙 (DFS)
        # 各ショップを出発点として探索
        PATH_LIMIT_LENGTH = 16  # 経路長の絶対的な上限
        
        for start_shop in range(self.K):
            self.cached_paths[start_shop] = []
            
            # DFS Stack: (current_node, path_list)
            stack = [(start_shop, [start_shop])]
            
            while stack:
                curr, path = stack.pop()
                
                # 枝刈り: 長すぎる場合
                if len(path) > PATH_LIMIT_LENGTH:
                    continue
                
                # 隣接頂点へ
                for neighbor in self.adj[curr]:
                    # パス内での重複チェック（閉路防止）
                    if neighbor in path:
                        continue
                    
                    # ショップに到達した場合
                    if self.is_shop(neighbor):
                        # パスとして保存するかの判定
                        min_d = self.dist_matrix[start_shop][neighbor]
                        if len(path) <= max(min_d * 2.0 + 2, 6): 
                            # パス全体を保存 (start ... end)
                            full_path = path + [neighbor]
                            self.cached_paths[start_shop].append((neighbor, full_path))
                        
                        # ショップに着いたら、そこから先へは進まない
                        continue
                    
                    # 木の場合、探索続行
                    stack.append((neighbor, path + [neighbor]))

    def solve(self):
        """
        メインループ
        """
        for t in range(self.T):
            action = -2 # 未定
            
            # 1. 実行中のパスがあればそれを進める
            if self.move_queue:
                action = self.move_queue.popleft()
            
            else:
                # 2. 次の行動を決定する
                
                # A. ショップにいる場合 -> キャッシュから最適なパスを探す
                best_path = None
                if self.is_shop(self.current_pos):
                    best_path = self.select_best_path()
                
                if best_path:
                    # 採用したパスをキューに入れる
                    # path[0]は現在地なので除く
                    for node in best_path[1:]:
                        self.move_queue.append(node)
                    action = self.move_queue.popleft()
                else:
                    # B. 有効なパスがない、または木の上にいる場合
                    
                    # まず味変を検討（まだやるべきことがあれば）
                    if self.plan_flavor_change():
                        action = self.move_queue.popleft()
                    else:
                        # C. 味変もできない -> 最寄りのショップへ戻る (リカバリー)
                        # ランダム移動ではなく、確実にショップを目指すことで無限ループを防ぐ
                        action = self.get_safe_move_to_nearest_shop()

            # --- 実行と出力 ---
            if action == -1:
                print("-1")
                if self.is_tree(self.current_pos):
                    self.tree_flavors[self.current_pos] = 'R'
                # 行動2は移動ではないため prev_pos は更新しない
            else:
                # 安全装置: Uターンチェック
                if action == self.prev_pos:
                    # 万が一Uターンになりそうな場合は、別の隣接点へ緊急回避
                    valid_moves = [v for v in self.adj[self.current_pos] if v != self.prev_pos]
                    if valid_moves:
                        action = valid_moves[0]
                    # valid_movesがない（次数1かつprev_posが唯一の隣接）場合は詰みだが、
                    # 2-辺連結グラフの性質上、必ず道はあるはず。
                
                print(f"{action}")
                self.execute_move(action)
            
            sys.stdout.flush()

    def select_best_path(self) -> Optional[List[int]]:
        """
        現在地から出発するキャッシュ済み全経路を評価し、
        「未取得の文字列」が得られる最も効率的な（短い）パスを返す。
        """
        start_node = self.current_pos
        if start_node not in self.cached_paths:
            return None
        
        best_path = None
        min_len = 9999
        
        for target_shop, path in self.cached_paths[start_node]:
            # 【重要】Uターン禁止チェック
            # パスの最初の移動先 path[1] が、直前に居た場所 prev_pos と同じならアウト
            if len(path) > 1 and path[1] == self.prev_pos:
                continue
            
            ice_chars = []
            for node in path[1:-1]: # 最初と最後を除く
                flavor = self.tree_flavors[node]
                ice_chars.append(flavor)
            
            generated_ice = "".join(ice_chars)
            
            if generated_ice not in self.shop_inventories[target_shop]:
                if len(path) < min_len:
                    min_len = len(path)
                    best_path = path
                    if min_len <= self.dist_matrix[start_node][target_shop] + 2:
                        return best_path

        return best_path

    def plan_flavor_change(self) -> bool:
        """
        有効なパスがない場合、近くの「Rに変えたい木」へ移動して味変する計画を立てる。
        味変後は、必ず最寄りのショップへ戻るまでのルートも含めて計画する。
        """
        # 候補: 戦略的にRにしたくて、まだWの場所
        candidates = [v for v in self.setup_candidates if self.tree_flavors[v] == 'W']
        
        if not candidates:
            return False

        # 1. 最寄りの候補地を探す
        queue = deque([(self.current_pos, [])])
        visited = {self.current_pos}
        
        target_candidate = -1
        path_to_candidate = []

        while queue:
            curr, path = queue.popleft()
            # 探索範囲を少し広げる
            if len(path) > 20: continue

            # 次のステップ候補
            next_nodes = []
            for neighbor in self.adj[curr]:
                # 初手でのUターンチェック
                if len(path) == 0 and neighbor == self.prev_pos:
                    continue
                next_nodes.append(neighbor)

            for neighbor in next_nodes:
                if neighbor in candidates:
                    target_candidate = neighbor
                    path_to_candidate = path + [neighbor]
                    break
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
            
            if target_candidate != -1:
                break
        
        if target_candidate == -1:
            return False

        # 2. 候補地から最寄りのショップへの帰還ルートを探す
        arrival_prev_pos = path_to_candidate[-2] if len(path_to_candidate) >= 2 else self.current_pos
        if len(path_to_candidate) == 1:
             arrival_prev_pos = self.current_pos
        
        if not path_to_candidate and self.current_pos == target_candidate:
            arrival_prev_pos = self.prev_pos

        # 帰還ルート探索BFS
        q_back = deque([(target_candidate, [])])
        v_back = {target_candidate}
        path_back = []
        
        while q_back:
            curr, path = q_back.popleft()
            # 探索範囲を少し広げる
            if len(path) > 20: break
            
            if self.is_shop(curr) and curr != target_candidate:
                path_back = path
                break
            
            for neighbor in self.adj[curr]:
                # Uターンチェック
                if len(path) == 0 and neighbor == arrival_prev_pos:
                    continue
                
                if neighbor not in v_back:
                    v_back.add(neighbor)
                    q_back.append((neighbor, path + [neighbor]))
            
            if path_back: break
        
        if not path_back:
            return False

        # 3. move_queue に登録
        for node in path_to_candidate:
            self.move_queue.append(node)
        self.move_queue.append(-1) # 味変
        for node in path_back:
            self.move_queue.append(node)
            
        return True

    def get_safe_move_to_nearest_shop(self) -> int:
        """
        現在地から最寄りのショップへ、Uターンせずに戻るための次の一手を返す。
        パスが見つからない場合は安全な隣接点を返す。
        """
        queue = deque([(self.current_pos, [])])
        visited = {self.current_pos}
        
        while queue:
            curr, path = queue.popleft()
            if len(path) > 20: break # あまり遠すぎても仕方ない
            
            # ゴール判定 (ただし初手でショップに居る場合は除く)
            if self.is_shop(curr) and (len(path) > 0 or self.current_pos != curr):
                if len(path) > 0:
                    return path[0]
            
            for neighbor in self.adj[curr]:
                # 初手Uターン禁止
                if len(path) == 0 and neighbor == self.prev_pos:
                    continue
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        
        # ショップが見つからない、または到達不能な場合
        # とりあえずUターンにならない隣接点へ進む
        valid_neighbors = [v for v in self.adj[self.current_pos] if v != self.prev_pos]
        if valid_neighbors:
            return valid_neighbors[0]
        
        # 完全に詰んだ場合（通常ありえない）
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

    def is_tree(self, v: int) -> bool:
        return v >= self.K

    def is_shop(self, v: int) -> bool:
        return v < self.K

if __name__ == "__main__":
    solver = IceCreamSolver()
    solver.solve()