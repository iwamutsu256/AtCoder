import sys
import collections
import random
import time
import math
import heapq

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1.20: v19 SAなし)

    コンセプト (v20):
    - v19 (main19.py) の SA (Step 4) を削除。
    - W[i,j] (Step 2) を「単純な訪問回数」に変更。
    - Step 3 (Cヒューリスティック) は維持。
    - Step 4 (SA) の代わりに、「貪欲ビンパッキング」
      (重いマスから、最も負荷が軽い色 c に割り当てる) で grid を決定。
    - Step 5 (ルール生成) を、ループしない
      「(c, k) -> q マッピング」を用いたシミュレーションに書き換え。
    """

    def __init__(self):
        """
        入力の読み込みと初期化 (main19 と同じ)
        """
        self.START_TIME = time.time()
        self.TIME_LIMIT = 1.8 

        self.N, self.K, self.T = map(int, sys.stdin.readline().split())
        self.v_walls = [sys.stdin.readline().strip() for _ in range(self.N)]
        self.h_walls = [sys.stdin.readline().strip() for _ in range(self.N - 1)]
        self.targets = [tuple(map(int, sys.stdin.readline().split())) for _ in range(self.K)]

        self.DIJ = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1), 'S': (0, 0)}
        self.DIR_CHARS = "UDLRS"
        
        self.direction_fields = []
        for k in range(self.K - 1):
            dir_field, _ = self.calculate_fields(self.targets[k + 1])
            self.direction_fields.append(dir_field)
        dummy_dir_field = [['S'] * self.N for _ in range(self.N)]
        self.direction_fields.append(dummy_dir_field)

    def can_move(self, i, j, d):
        """
        マス(i, j)から方向dに移動可能か（壁がないか）を判定する (main19 と同じ)
        """
        if d == 'U':
            return i > 0 and self.h_walls[i - 1][j] == '0'
        if d == 'D':
            return i < self.N - 1 and self.h_walls[i][j] == '0'
        if d == 'L':
            return j > 0 and self.v_walls[i][j - 1] == '0'
        if d == 'R':
            return j < self.N - 1 and self.v_walls[i][j] == '0'
        if d == 'S':
            return True
        return False

    def calculate_fields(self, target_pos):
        """
        指定された目的地 target_pos からBFSを行い、
        「最適移動方向」と「最短距離」のフィールドを計算する。 (main19 と同じ)
        """
        tr, tc = target_pos
        dist = [[float('inf')] * self.N for _ in range(self.N)]
        direction_field = [['S'] * self.N for _ in range(self.N)]
        q = collections.deque()
        q.append(target_pos)
        dist[tr][tc] = 0
        while q:
            r, c = q.popleft()
            for d in self.DIR_CHARS:
                if d == 'S': continue
                di, dj = self.DIJ[d]
                nr, nc = r - di, c - dj 
                if not (0 <= nr < self.N and 0 <= nc < self.N):
                    continue
                if not self.can_move(nr, nc, d):
                    continue
                if dist[nr][nc] == float('inf'):
                    dist[nr][nc] = dist[r][c] + 1
                    direction_field[nr][nc] = d
                    q.append((nr, nc))
        return direction_field, dist
    
    def get_pos_after_move(self, i, j, D):
        """
        (i, j) から D に移動した (壁考慮) 後の座標を返す (main19 と同じ)
        """
        if self.can_move(i, j, D):
            di, dj = self.DIJ[D]
            return i + di, j + dj
        else:
            return i, j # 壁なら移動しない

    def solve(self):
        """
        メイン処理 (v20)
        """
        
        # --- 1. K-1 本の経路 (P_k) を計算 ---
        # (main19 と同じ)
        all_paths = [] 
        for k in range(self.K - 1): 
            path_k = []
            q = k
            ci, cj = self.targets[k]
            gi, gj = self.targets[k + 1]
            current_steps_for_path = 0
            while (ci, cj) != (gi, gj):
                path_k.append((ci, cj))
                D = self.direction_fields[q][ci][cj]
                if D == 'S': break 
                if not self.can_move(ci, cj, D): break 
                di, dj = self.DIJ[D]
                ci, cj = ci + di, cj + dj
                current_steps_for_path += 1
                if current_steps_for_path > self.N * self.N: break 
            path_k.append((ci, cj))
            all_paths.append(path_k)
        
        # --- 2. (v20) 「単純な訪問回数」 W[i,j] の計算 ---
        W = collections.defaultdict(int)
        all_cells_list_unique = set()
        
        for k in range(self.K - 1):
            for pos in all_paths[k]:
                W[pos] += 1 # 単純な訪問回数
                all_cells_list_unique.add(pos)

        # --- 3. (v19) 最小 C のヒューリスティック計算 ---
        X = sum(W.values()) # 必要な全スロット数
        if not X: X = 1
        
        max_w = max(W.values()) if W else 1
        
        C_target = int(math.ceil(X / max_w))
        C_final = min(max(C_target, 1), self.N*self.N, self.T+1)
        self.C = C_final

        # --- 4. (v20) 貪欲ビンパッキング (SAの代わり) ---
        
        # q_cost[c] = 色 c の負荷 (割り当てられた W の合計)
        q_cost = [0] * self.C
        best_grid = [[0] * self.N for _ in range(self.N)] # 盤面
        
        # W (訪問回数) が多いマスから順に割り当てる
        sorted_cells = sorted(list(all_cells_list_unique), key=lambda pos: W[pos], reverse=True)
        
        for pos in sorted_cells:
            # 最も負荷が軽い色 (min_c) を探す
            min_c = 0
            min_load = q_cost[0]
            for c_search in range(1, self.C):
                if q_cost[c_search] < min_load:
                    min_load = q_cost[c_search]
                    min_c = c_search
            
            # (pos) を (min_c) に割り当て
            best_grid[pos[0]][pos[1]] = min_c
            q_cost[min_c] += W[pos]
        
        # この貪欲割り当てで必要になった Q
        self.Q_final = max(q_cost) if q_cost else 1


        # --- 5. (v20) ループ回避ルール生成 (Tステップシミュレーション) ---
        
        rules = {} # (c, q) -> (A, S_q, D)
        
        # (v20) q_map[(c, k)] = q
        # (「色c」で「経路k」を実行中」 -> どの「qスロット」を使うか)
        q_map = {}
        q_counter = [0] * self.C # c ごとの q スロットカウンター
        
        current_i, current_j = self.targets[0]
        current_k = 0 
        visited_count = 1
        
        for step in range(self.T):
            pos = (current_i, current_j)
            k = current_k
            
            c = best_grid[pos[0]][pos[1]] # 貪欲割り当てで決めた色
            
            # --- (A) (c, q) スロットの割り当て ---
            # (色c, 経路k) のペアから、ユニークな q を決定
            key = (c, k) 
            if key not in q_map:
                q = q_counter[c]
                q_map[key] = q
                q_counter[c] += 1
            
            q = q_map[key]
            
            # (貪欲割り当てが Q_final を超えた場合の保険)
            if q >= self.Q_final:
                q = self.Q_final - 1 

            # --- (B) S (次のq) の計算 ---
            if (c, q) not in rules:
                A_req = c
                target_pos = self.targets[k + 1]
                
                S_req_k = k # 次の経路 (Default: stay)
                D_req = self.direction_fields[k][pos[0]][pos[1]]
                
                if pos == target_pos:
                    S_req_k = k + 1 # 次の経路へ
                    D_req = self.direction_fields[k + 1][pos[0]][pos[1]]
                    if S_req_k == self.K: # 最後の目的地
                        S_req_k = self.K - 1
                        D_req = 'S'

                # --- 次の (c, q) を計算 ---
                pos_next = self.get_pos_after_move(pos[0], pos[1], D_req)
                c_next = best_grid[pos_next[0]][pos_next[1]]
                k_next = S_req_k
                
                key_next = (c_next, k_next)
                if key_next not in q_map:
                    q_next = q_counter[c_next]
                    q_map[key_next] = q_next
                    q_counter[c_next] += 1
                q_next = q_map[key_next]
                
                if q_next >= self.Q_final:
                    q_next = self.Q_final - 1

                S_final_q = q_next
                rules[(c, q)] = (A_req, S_final_q, D_req)
            
            # --- (C) 実行 ---
            A, S, D = rules[(c, q)]
            
            # (v19 の失敗点: current_q は S に従う)
            # (v20 では current_k (経路) のみが重要)
            
            if pos == target_pos:
                current_k += 1
                if current_k == self.K: # 完了
                   break
            
            current_i, current_j = self.get_pos_after_move(pos[0], pos[1], D)
            
            # --- (D) V カウント (v17 と同じ) ---
            if visited_count < self.K:
                next_target_index = visited_count
                if (current_i, current_j) == self.targets[next_target_index]:
                    visited_count += 1
                    if visited_count == self.K:
                        break
        
        self.V = visited_count
        self.C_final = C_final
        # (v20) Q_final を、実際に使ったスロット数で再計算
        self.Q_final = max(q_counter) if q_counter else 1


        # --- 6. 出力 ---
        initial_grid = best_grid

        # --- スコア計算 (stderr) ---
        final_score = 0
        if self.V == self.K:
            final_score = self.C_final + self.Q_final
        else:
            final_score = 2 * (self.N**4) + (self.K - self.V) * (self.N**2)
        print(final_score, file=sys.stderr)

        # --- 回答 (stdout) ---
        print(self.C_final, self.Q_final, len(rules))
        for row in initial_grid:
            print(' '.join(map(str, row)))
        for (c, q), (A, S, D) in rules.items():
            print(c, q, A, S, D)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()