import sys
import math
import random
import time
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

# ------------------------------------------------------------------------------
# クラス・関数定義
# ------------------------------------------------------------------------------

class IceCreamSolver:
    """
    AHC 'Ice Cream Collection' 問題を解くためのソルバークラス。
    
    【機能構成】
    1. 事前計算: 全点対間距離と、有効な経路（パス）の列挙・キャッシュ。
    2. 戦略最適化: 焼きなまし法により、どの木をRにするべきかの理想配置(target_flavors)を決定。
    3. 実行: キャッシュされたパスと最適化された戦略に基づき、シミュレーションを行いながら移動。
    """

    def __init__(self):
        """初期化と入力受取"""
        self.start_time = time.time() # 開始時刻の記録
        
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
        
        # 木の初期味はすべて 'W' (実際の盤面)
        self.tree_flavors: List[Optional[str]] = [None] * self.N
        for i in range(self.K, self.N):
            self.tree_flavors[i] = 'W'

        self.current_ice_cream = ""
        self.current_pos = 0
        self.prev_pos = -1
        
        # 移動キュー (決定済みのパス)
        self.move_queue = deque()
        
        # 経路キャッシュ
        # key: start_shop_index, value: list of (end_shop_index, path_list)
        self.cached_paths: Dict[int, List[Tuple[int, List[int]]]] = {}
        
        # 1. 事前計算の実行
        self.precompute_all_paths()
        
        # 2. 戦略(target_flavors)の初期化と焼きなまし最適化
        # まずはランダムで初期化
        self.target_flavors: List[Optional[str]] = [None] * self.N
        self.setup_candidates = set()
        
        # 焼きなまし法で target_flavors を最適化 (1.5秒ほど使用)
        self.optimize_strategy(time_limit=1.5)
        
        # 最適化結果に基づき setup_candidates を構築
        for i in range(self.K, self.N):
            if self.target_flavors[i] == 'R':
                self.setup_candidates.add(i)

    def precompute_all_paths(self):
        """
        ショップ間の有効な経路を事前に列挙・保存する。
        """
        # 全点対間最短距離 (Warshall-Floyd)
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

        # パス列挙 (DFS)
        PATH_LIMIT_LENGTH = 16
        
        for start_shop in range(self.K):
            self.cached_paths[start_shop] = []
            stack = [(start_shop, [start_shop])]
            
            while stack:
                curr, path = stack.pop()
                if len(path) > PATH_LIMIT_LENGTH: continue
                
                for neighbor in self.adj[curr]:
                    if neighbor in path: continue
                    
                    if self.is_shop(neighbor):
                        min_d = self.dist_matrix[start_shop][neighbor]
                        if len(path) <= max(min_d * 2.0 + 2, 6): 
                            full_path = path + [neighbor]
                            self.cached_paths[start_shop].append((neighbor, full_path))
                        continue
                    
                    stack.append((neighbor, path + [neighbor]))

    def optimize_strategy(self, time_limit: float):
        """
        【焼きなまし法】
        target_flavors（どの木をRにするかの計画）を最適化する。
        評価関数: 現在のキャッシュされたパスを使って、
        「短い距離で」いくつのユニークな文字列を作れるか（距離重み付き）。
        
        近傍操作:
        1. Flip: 1つの木の味を反転 (増減)
        2. Swap: Rの木とWの木を入れ替え (配置変更)
        """
        # 初期解生成（ランダム）
        # Rの比率も少しランダムに振る
        current_targets = {}
        initial_r_prob = random.uniform(0.3, 0.7)
        for i in range(self.K, self.N):
            current_targets[i] = 'R' if random.random() < initial_r_prob else 'W'
        
        # 現在のスコア計算
        current_score = self.calc_static_score(current_targets)
        best_score = current_score
        best_targets = current_targets.copy()
        
        # 温度設定
        start_temp = 100.0
        end_temp = 0.1
        
        # ループ開始
        iter_count = 0
        
        # Swap用の頂点リスト管理はコストがかかるので、ランダムピックで対応する
        
        while True:
            iter_count += 1
            if iter_count % 100 == 0:
                elapsed = time.time() - self.start_time
                if elapsed > time_limit:
                    break
            
            # --- 近傍選択 ---
            # 50%でFlip, 50%でSwap
            mode = random.random()
            
            op_type = 'none'
            u, v = -1, -1
            original_u_flavor = ''
            original_v_flavor = ''

            # Mode 1: Flip (1点反転)
            if mode < 0.5:
                op_type = 'flip'
                u = random.randint(self.K, self.N - 1)
                original_u_flavor = current_targets[u]
                new_flavor = 'R' if original_u_flavor == 'W' else 'W'
                current_targets[u] = new_flavor
                
            # Mode 2: Swap (2点交換)
            else:
                op_type = 'swap'
                u = random.randint(self.K, self.N - 1)
                v = random.randint(self.K, self.N - 1)
                
                # 異なる味同士ならSwap実行
                if current_targets[u] != current_targets[v]:
                    original_u_flavor = current_targets[u]
                    original_v_flavor = current_targets[v]
                    current_targets[u], current_targets[v] = current_targets[v], current_targets[u]
                else:
                    # 同じ味なら何もしない（実質無効な遷移だが、今回はSkip扱い）
                    op_type = 'none'

            if op_type == 'none':
                continue

            # スコア再計算
            new_score = self.calc_static_score(current_targets)
            
            # 遷移判定
            delta = new_score - current_score
            
            # 現在の温度 (OverflowError対策済)
            elapsed = time.time() - self.start_time
            if elapsed >= time_limit:
                 progress = 1.0
            else:
                 progress = elapsed / time_limit
                 
            temp = start_temp + (end_temp - start_temp) * progress
            temp = max(temp, 0.001)
            
            accept = False
            if delta > 0:
                accept = True
            else:
                try:
                    prob = math.exp(delta / temp)
                except OverflowError:
                    prob = 0
                accept = prob > random.random()

            if accept:
                current_score = new_score
                if current_score > best_score:
                    best_score = current_score
                    best_targets = current_targets.copy()
            else:
                # 却下 (戻す)
                if op_type == 'flip':
                    current_targets[u] = original_u_flavor
                elif op_type == 'swap':
                    current_targets[u] = original_u_flavor
                    current_targets[v] = original_v_flavor

        # 結果を適用
        self.target_flavors = [None] * self.N
        for i in range(self.K, self.N):
            self.target_flavors[i] = best_targets[i]

    def calc_static_score(self, targets_map: Dict[int, str]) -> float:
        """
        評価関数改善版:
        単に種類数を数えるのではなく、「短いパスで作れる」ことにボーナスを与える。
        短い距離で多様なアイスを作れる配置ほど高得点。
        """
        total_score = 0.0
        
        for start_shop in range(self.K):
            # 文字列ごとの最短パス長を記録
            string_min_lens = {}
            
            for _, path in self.cached_paths[start_shop]:
                # パスに対応する文字列を生成
                chars = []
                for node in path[1:-1]:
                    chars.append(targets_map[node])
                s = "".join(chars)
                
                length = len(path)
                if s not in string_min_lens or length < string_min_lens[s]:
                    string_min_lens[s] = length
            
            # スコア加算
            for length in string_min_lens.values():
                # 距離の逆数などで重み付け: 近いほど価値が高い
                total_score += 100.0 / length
            
        return total_score

    def solve(self):
        """
        メインループ
        """
        for t in range(self.T):
            action = -2 # 未定
            
            if self.move_queue:
                action = self.move_queue.popleft()
            else:
                # 行動決定
                best_path = None
                if self.is_shop(self.current_pos):
                    best_path = self.select_best_path()
                
                if best_path:
                    for node in best_path[1:]:
                        self.move_queue.append(node)
                    action = self.move_queue.popleft()
                else:
                    if self.plan_flavor_change():
                        action = self.move_queue.popleft()
                    else:
                        if self.plan_recovery_move():
                            action = self.move_queue.popleft()
                        else:
                            valid_moves = [v for v in self.adj[self.current_pos] if v != self.prev_pos]
                            if valid_moves:
                                action = random.choice(valid_moves)
                            else:
                                action = self.adj[self.current_pos][0]

            # 実行
            if action == -1:
                print("-1")
                if self.is_tree(self.current_pos):
                    self.tree_flavors[self.current_pos] = 'R'
            else:
                if action == self.prev_pos:
                    valid_moves = [v for v in self.adj[self.current_pos] if v != self.prev_pos]
                    if valid_moves:
                        action = valid_moves[0]
                
                print(f"{action}")
                self.execute_move(action)
            
            sys.stdout.flush()

    def select_best_path(self) -> Optional[List[int]]:
        """現在の状況で最適なパスを選択"""
        start_node = self.current_pos
        if start_node not in self.cached_paths:
            return None
        
        best_path = None
        min_len = 9999
        
        for target_shop, path in self.cached_paths[start_node]:
            # Uターンチェック
            if len(path) > 1 and path[1] == self.prev_pos:
                continue
            
            ice_chars = []
            for node in path[1:-1]:
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
        """味変計画"""
        candidates = [v for v in self.setup_candidates if self.tree_flavors[v] == 'W']
        if not candidates: return False

        queue = deque([(self.current_pos, [])])
        visited = {self.current_pos}
        target_candidate = -1
        path_to_candidate = []

        while queue:
            curr, path = queue.popleft()
            if len(path) > 20: continue
            
            next_nodes = []
            for neighbor in self.adj[curr]:
                if len(path) == 0 and neighbor == self.prev_pos: continue
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
            if target_candidate != -1: break
        
        if target_candidate == -1: return False

        arrival_prev_pos = path_to_candidate[-2] if len(path_to_candidate) >= 2 else self.current_pos
        if len(path_to_candidate) == 1: arrival_prev_pos = self.current_pos
        if not path_to_candidate and self.current_pos == target_candidate: arrival_prev_pos = self.prev_pos

        q_back = deque([(target_candidate, [])])
        v_back = {target_candidate}
        path_back = []
        
        while q_back:
            curr, path = q_back.popleft()
            if len(path) > 20: break
            if self.is_shop(curr) and curr != target_candidate:
                path_back = path
                break
            for neighbor in self.adj[curr]:
                if len(path) == 0 and neighbor == arrival_prev_pos: continue
                if neighbor not in v_back:
                    v_back.add(neighbor)
                    q_back.append((neighbor, path + [neighbor]))
            if path_back: break
        
        if not path_back: return False

        for node in path_to_candidate: self.move_queue.append(node)
        self.move_queue.append(-1)
        for node in path_back: self.move_queue.append(node)
        return True

    def plan_recovery_move(self) -> bool:
        """リカバリー移動"""
        if self.is_shop(self.current_pos):
            candidates = [s for s in range(self.K) if s != self.current_pos]
        else:
            candidates = list(range(self.K))
        if not candidates: return False
        random.shuffle(candidates)
        
        for target_shop in candidates:
            queue = deque([(self.current_pos, [])])
            visited = {self.current_pos}
            while queue:
                curr, path = queue.popleft()
                if len(path) > 30: continue
                if curr == target_shop:
                    for node in path: self.move_queue.append(node)
                    return True
                for neighbor in self.adj[curr]:
                    if len(path) == 0 and neighbor == self.prev_pos: continue
                    if self.is_shop(neighbor) and neighbor != target_shop: continue
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
        return False

    def execute_move(self, v: int):
        self.prev_pos = self.current_pos
        self.current_pos = v
        if self.is_tree(v):
            self.current_ice_cream += self.tree_flavors[v]
        else:
            if self.current_ice_cream not in self.shop_inventories[v]:
                self.shop_inventories[v].add(self.current_ice_cream)
            self.current_ice_cream = ""

    def is_tree(self, v: int) -> bool: return v >= self.K
    def is_shop(self, v: int) -> bool: return v < self.K

if __name__ == "__main__":
    solver = IceCreamSolver()
    solver.solve()