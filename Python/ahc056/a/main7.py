import sys
import collections
import time
import math

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1.11: v10バグ修正)

    コンセプト (v11):
    - v10 の Q圧縮 (Step 2) ロジックは維持する。
    - v10 のバグ (タイポ new_c) を修正。
    - v10 のバグ (M > T): Step 4 のルール生成が T を超えていた。
    
    修正点 (v11):
    - Step 4 (ルール生成) を、T ステップの「シミュレーション」ベースに戻す。
    - Q圧縮 (final_q_map) と 色付け (visited_cells_map) を
      T ステップシミュレーションの中で同時に行う。
    - これにより M <= T を厳格に保証する。
    """

    def __init__(self):
        """
        入力の読み込みと初期化 (main10 と同じ)
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
        # 完了状態 (K-1) 用のダミー (q=K-1 -> q=K-1)
        # (v11 では K-1 への方向場は使わないが、
        #  K-2 -> K-1 の方向場 (direction_fields[K-2]) は使う)
        dummy_dir_field = [['S'] * self.N for _ in range(self.N)]
        self.direction_fields.append(dummy_dir_field)

    def can_move(self, i, j, d):
        """
        マス(i, j)から方向dに移動可能か（壁がないか）を判定する (main10 と同じ)
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
        「最適移動方向」と「最短距離」のフィールドを計算する。 (main10 と同じ)
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
        メイン処理 (v11):
        1. K-1 本の経路 (P_k) と使用マスセット (C_k) を計算
        2. (v9) 厳格なグループマージで Q圧縮 (q_map 作成) (v10タイポ修正)
        3. (v11) Tステップシミュレーション (V計算 と M<=Tルール生成 を同時に)
        4. 出力
        """
        
        # --- 1. K-1 本の経路 (P_k) と使用マスセット (C_k) を計算 ---
        # (main10 と同じ)
        all_paths = [] 
        all_cells = [] 
        global_total_steps = 0
        
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
            global_total_steps += (len(path_k) - 1)

        # --- 2. Q 圧縮 (v9: 厳格なグループマージ) ---
        # (main10 と同じ)
        q_map_raw = list(range(self.K - 1)) 
        groups = {k: {k} for k in range(self.K - 1)} 
        for i in range(self.K - 1):
            if i not in groups: continue
            for j in range(i + 1, self.K - 1):
                if j not in groups: continue
                can_merge = True
                for k_in_group_i in groups[i]:
                    for k_in_group_j in groups[j]:
                        if not all_cells[k_in_group_i].isdisjoint(all_cells[k_in_group_j]):
                            can_merge = False
                            break
                    if not can_merge:
                        break
                if can_merge:
                    root_i, root_j = i, j
                    if len(groups[root_i]) < len(groups[root_j]):
                        root_i, root_j = root_j, root_i 
                    for k_j in groups[root_j]:
                        q_map_raw[k_j] = root_i
                    groups[root_i].update(groups[root_j])
                    del groups[root_j] 
        
        unique_q_values = sorted(list(set(q_map_raw)))
        
        # (v10 タイポ修正: new_c -> new_q)
        q_remap = {old_q: new_q for new_q, old_q in enumerate(unique_q_values)}
        
        Q_new = len(unique_q_values) + 1 
        final_q_map = [0] * self.K
        for k in range(self.K - 1):
            final_q_map[k] = q_remap[q_map_raw[k]]
        final_q_map[self.K - 1] = Q_new - 1 
        self.Q_final = Q_new


        # --- 3. (v11) Tステップシミュレーション (V計算 と M<=Tルール生成) ---
        
        rules = {} 
        visited_cells_map = {} 
        current_color_id = 0
        
        current_i, current_j = self.targets[0]
        
        # (重要) current_k は「次に目指す目的地の *元の* index」 (k=0..K-1)
        # k=0: target_0 にいる (V=1)
        current_k = 0 
        
        # マッピング後の状態 (q_new)
        current_q_mapped = final_q_map[current_k]
        
        # V (訪問済み目的地数)
        visited_count = 1 
        
        for step in range(self.T):
            
            # --- 1. 色の割り当て (main3 と同じ) ---
            pos = (current_i, current_j)
            if pos not in visited_cells_map:
                visited_cells_map[pos] = current_color_id
                current_color_id += 1
            
            c = visited_cells_map[pos]
            q = current_q_mapped # マッピング後の状態
            
            # --- 2. 完了状態 (q_new) か？ ---
            if q == self.Q_final - 1:
                # 最後の目的地に到着済み (V=K)
                if (c, q) not in rules:
                    rules[(c, q)] = (c, q, 'S')
                break # シミュレーション終了
            
            # --- 3. ルール決定 (v11 核心部) ---
            if (c, q) not in rules:
                
                # (重要) q はマッピング後の状態だが、
                # どの方角 (BFS) を見るかは、マッピング前の k に依存する
                
                target_pos = self.targets[current_k + 1] # 次に目指す目的地
                
                if pos == target_pos:
                    # --- 目的地 (target_{k+1}) に到達 ---
                    A = c
                    current_k += 1 # 次の目的地 (k+1) を目指す
                    S = final_q_map[current_k] # (k+1) のマッピング先状態
                    
                    if S == self.Q_final - 1:
                        # これが最後の目的地 (target_{K-1}) だった
                        D = 'S'
                    else:
                        # (k+1) -> (k+2) への移動
                        # (direction_fields[k+1] を参照)
                        D = self.direction_fields[current_k][pos[0]][pos[1]]
                
                else:
                    # --- 移動中 ---
                    A = c
                    S = q # 状態 (q_new) はそのまま
                    # k -> (k+1) への移動
                    # (direction_fields[k] を参照)
                    D = self.direction_fields[current_k][pos[0]][pos[1]]
                    
                rules[(c, q)] = (A, S, D)

            # --- 4. 実行 ---
            A, S, D = rules[(c, q)]
            
            current_q_mapped = S # 状態 (q_new) を更新
            
            if self.can_move(current_i, current_j, D):
                di, dj = self.DIJ[D]
                current_i += di
                current_j += dj
            
            # --- 5. V カウント (main3.py と同じ) ---
            if visited_count < self.K:
                next_target_index = visited_count
                if (current_i, current_j) == self.targets[next_target_index]:
                    visited_count += 1
        
        self.V = visited_count
        self.C = current_color_id


        # --- 5. 出力 ---
        # (main10 と同じ)
        initial_grid = [[0] * self.N for _ in range(self.N)]
        for (i, j), color in visited_cells_map.items():
            initial_grid[i][j] = color

        # --- スコア計算 (stderr) ---
        final_score = 0
        if self.V == self.K:
            final_score = self.C + self.Q_final
        else:
            final_score = 2 * (self.N**4) + (self.K - self.V) * (self.N**2)
        print(final_score, file=sys.stderr)

        # --- 回答 (stdout) ---
        print(self.C, self.Q_final, len(rules))
        for row in initial_grid:
            print(' '.join(map(str, row)))
        for (c, q), (A, S, D) in rules.items():
            print(c, q, A, S, D)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()