import sys
import collections
import time
import math

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1.12: Q圧縮 + C圧縮)

    コンセプト (v12):
    - v11 (main11.py) の Q圧縮ロジックは成功した (ヒートマップが縦長に)。
    - ユーザーの観察: 「新しい色(C)の行に空きが多い」
    - 提案: C (色) についても、Q と同じ「厳格なグループマージ」を行い、
      C と Q の両方を圧縮する。
    
    手順:
    1. (v11) Q圧縮のための経路計算
    2. (v11) Qの厳格なグループマージ (final_q_map 作成)
    3. (v11) Tステップシミュレーション (V計算 と M<=Tルール, C_old色 を生成)
    4. (NEW) Cの厳格なグループマージ
       - rules をスキャンし、color_usage[c] = {q} を作成
       - v9 と同じロジックで c=0..C_old-1 をマージ (color_map 作成)
    5. C_new と Q_final を使ってリマップし、出力
    """

    def __init__(self):
        """
        入力の読み込みと初期化 (main11 と同じ)
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
        マス(i, j)から方向dに移動可能か（壁がないか）を判定する (main11 と同じ)
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
        「最適移動方向」と「最短距離」のフィールドを計算する。 (main11 と同じ)
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
        
    def solve(self):
        """
        メイン処理 (v12):
        1. (v11) Q圧縮のための経路計算
        2. (v11) Qの厳格なグループマージ (final_q_map 作成)
        3. (v11) Tステップシミュレーション (V計算 と M<=Tルール, C_old色 を生成)
        4. (NEW) Cの厳格なグループマージ (final_c_map 作成)
        5. C_new と Q_new を使ってリマップし、出力
        """
        
        # --- 1. K-1 本の経路 (P_k) と使用マスセット (C_k) を計算 ---
        # (main11 と同じ)
        all_paths = [] 
        all_cells = [] 
        
        for k in range(self.K - 1): 
            path_k = []
            cells_k = set()
            q = k
            ci, cj = self.targets[k]
            gi, gj = self.targets[k + 1]
            current_steps_for_path = 0
            
            while (ci, cj) != (gi, gj):
                path_k.append((ci, cj))
                cells_k.add((ci, cj))
                D = self.direction_fields[q][ci][cj]
                if D == 'S': break 
                if not self.can_move(ci, cj, D): break 
                di, dj = self.DIJ[D]
                ci, cj = ci + di, cj + dj
                current_steps_for_path += 1
                if current_steps_for_path > self.N * self.N: break 
            
            path_k.append((ci, cj))
            cells_k.add((ci, cj))
            all_paths.append(path_k)
            all_cells.append(cells_k)

        # --- 2. Q 圧縮 (v9: 厳格なグループマージ) ---
        # (main11 と同じ)
        q_map_raw = list(range(self.K - 1)) 
        q_groups = {k: {k} for k in range(self.K - 1)} 
        for i in range(self.K - 1):
            if i not in q_groups: continue
            for j in range(i + 1, self.K - 1):
                if j not in q_groups: continue
                can_merge = True
                for k_in_group_i in q_groups[i]:
                    for k_in_group_j in q_groups[j]:
                        if not all_cells[k_in_group_i].isdisjoint(all_cells[k_in_group_j]):
                            can_merge = False
                            break
                    if not can_merge:
                        break
                if can_merge:
                    root_i, root_j = i, j
                    if len(q_groups[root_i]) < len(q_groups[root_j]):
                        root_i, root_j = root_j, root_i 
                    for k_j in q_groups[root_j]:
                        q_map_raw[k_j] = root_i
                    q_groups[root_i].update(q_groups[root_j])
                    del q_groups[root_j] 
        
        unique_q_values = sorted(list(set(q_map_raw)))
        q_remap = {old_q: new_q for new_q, old_q in enumerate(unique_q_values)}
        Q_new = len(unique_q_values) + 1 
        final_q_map = [0] * self.K
        for k in range(self.K - 1):
            final_q_map[k] = q_remap[q_map_raw[k]]
        final_q_map[self.K - 1] = Q_new - 1 
        self.Q_final = Q_new

        # --- 3. (v11) Tステップシミュレーション (V計算 と M<=Tルール生成) ---
        # (main11 と同じ)
        rules = {} 
        visited_cells_map = {} 
        current_color_id = 0
        current_i, current_j = self.targets[0]
        current_k = 0 
        current_q_mapped = final_q_map[current_k]
        visited_count = 1 
        
        for step in range(self.T):
            pos = (current_i, current_j)
            if pos not in visited_cells_map:
                visited_cells_map[pos] = current_color_id
                current_color_id += 1
            c = visited_cells_map[pos]
            q = current_q_mapped 
            
            if q == self.Q_final - 1:
                if (c, q) not in rules:
                    rules[(c, q)] = (c, q, 'S')
                break 
            
            if (c, q) not in rules:
                target_pos = self.targets[current_k + 1]
                if pos == target_pos:
                    A = c
                    current_k += 1 
                    S = final_q_map[current_k]
                    if S == self.Q_final - 1:
                        D = 'S'
                    else:
                        D = self.direction_fields[current_k][pos[0]][pos[1]]
                else:
                    A = c
                    S = q 
                    D = self.direction_fields[current_k][pos[0]][pos[1]]
                rules[(c, q)] = (A, S, D)

            A, S, D = rules[(c, q)]
            current_q_mapped = S 
            if self.can_move(current_i, current_j, D):
                di, dj = self.DIJ[D]
                current_i += di
                current_j += dj
            
            if visited_count < self.K:
                next_target_index = visited_count
                if (current_i, current_j) == self.targets[next_target_index]:
                    visited_count += 1
        
        self.V = visited_count
        self.C_old = current_color_id # 圧縮前の色数
        
        # --- 4. (NEW) Cの厳格なグループマージ ---
        
        # 4a. color_usage[c] = {q} を作成
        color_usage = [set() for _ in range(self.C_old)]
        for (c, q) in rules.keys():
            if 0 <= c < self.C_old:
                color_usage[c].add(q)
        
        # 4b. C について厳格なグループマージ (v9ロジック)
        c_map_raw = list(range(self.C_old))
        c_groups = {c: {c} for c in range(self.C_old)}
        
        for i in range(self.C_old):
            if i not in c_groups: continue
            for j in range(i + 1, self.C_old):
                if j not in c_groups: continue
                
                can_merge = True
                for k_in_group_i in c_groups[i]:
                    for k_in_group_j in c_groups[j]:
                        if not color_usage[k_in_group_i].isdisjoint(color_usage[k_in_group_j]):
                            can_merge = False
                            break
                    if not can_merge:
                        break
                
                if can_merge:
                    root_i, root_j = i, j
                    if len(c_groups[root_i]) < len(c_groups[root_j]):
                        root_i, root_j = root_j, root_i
                    for k_j in c_groups[root_j]:
                        c_map_raw[k_j] = root_i
                    c_groups[root_i].update(c_groups[root_j])
                    del c_groups[root_j]

        # --- 5. C_new と Q_new を使ってリマップし、出力 ---
        
        # C のリマップ
        unique_c_values = sorted(list(set(c_map_raw)))
        c_remap = {old_c: new_c for new_c, old_c in enumerate(unique_c_values)}
        self.C_final = len(unique_c_values)
        if self.C_final == 0: self.C_final = 1 # (C >= 1 制約)

        # 5a. 最終的な盤面 (initial_grid) のリマップ
        initial_grid = [[0] * self.N for _ in range(self.N)]
        for (i, j), c_old in visited_cells_map.items():
            if 0 <= c_old < self.C_old:
                 initial_grid[i][j] = c_remap[c_map_raw[c_old]]
            # (else: 0 のまま)

        # 5b. 最終的なルール (rules) のリマップ
        final_rules = {}
        for (c_old, q_mapped), (A_old, S_mapped, D) in rules.items():
            
            if not (0 <= c_old < self.C_old): continue # (ありえないはず)
            
            c_new = c_remap[c_map_raw[c_old]]
            
            # (A=c 固定なので A_old も c_old と同じはず)
            A_new = c_new 
            
            # (q_mapped, S_mapped は Q_new にマッピング済み)
            final_rules[(c_new, q_mapped)] = (A_new, S_mapped, D)


        # --- スコア計算 (stderr) ---
        final_score = 0
        if self.V == self.K:
            final_score = self.C_final + self.Q_final
        else:
            final_score = 2 * (self.N**4) + (self.K - self.V) * (self.N**2)
        print(final_score, file=sys.stderr)

        # --- 回答 (stdout) ---
        print(self.C_final, self.Q_final, len(final_rules))
        for row in initial_grid:
            print(' '.join(map(str, row)))
        for (c, q), (A, S, D) in final_rules.items():
            print(c, q, A, S, D)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()