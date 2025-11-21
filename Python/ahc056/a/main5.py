import sys
import collections
import random
import time
import math

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 2: 焼きなまし法 v6)

    コンセプト (SA v6):
    - 初期解: main3.py (経路色付け貪欲法) の解 (s0, C0, Q0=K) を使用。
    - SAの目的: s0 をベースに、V=K を維持しつつ C (色数) を削減する。
    - 近傍操作:
        1. 色のマージ (C-1)
        2. 色の付け替え (Cは不変)
        3. 色の分離 (C+1, ただし C <= C0 まで)
    - エネルギー:
        - V == K なら C + Q (真のスコア)
        - V < K なら 2N^4 + (K-V)N^2 (ペナルティ)
    """

    def __init__(self):
        """
        入力の読み込みと初期化
        """
        self.START_TIME = time.time()
        self.TIME_LIMIT = 1.8 # 2.0秒制限に対し、マージンを持つ

        # --- 入力読み込み ---
        self.N, self.K, self.T = map(int, sys.stdin.readline().split())
        self.v_walls = [sys.stdin.readline().strip() for _ in range(self.N)]
        self.h_walls = [sys.stdin.readline().strip() for _ in range(self.N - 1)]
        self.targets = [tuple(map(int, sys.stdin.readline().split())) for _ in range(self.K)]

        # --- 内部状態 ---
        self.DIJ = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1), 'S': (0, 0)}
        self.DIR_CHARS = "UDLRS"
        
        self.Q = self.K # QはKで固定
        
        # --- アルゴリズム核心部 (事前計算) ---
        # 全ての目的地 k -> k+1 への方向場を事前に計算しておく
        self.direction_fields = []
        for k in range(self.K - 1):
            self.direction_fields.append(self.calculate_direction_field(self.targets[k + 1]))
        # 最後の目的地 k -> (k+1) (S=K-1) 用のダミー (すべて 'S')
        dummy_field = [['S'] * self.N for _ in range(self.N)]
        self.direction_fields.append(dummy_field)


    def can_move(self, i, j, d):
        """
        マス(i, j)から方向dに移動可能か（壁がないか）を判定する (main3.py と同じ)
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

    def calculate_direction_field(self, target_pos):
        """
        指定された目的地 target_pos からBFSを行い、
        全マスからの「最適移動方向」のフィールドを計算する。 (main3.py と同じ)
        """
        tr, tc = target_pos
        dist = [[-1] * self.N for _ in range(self.N)]
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
                if dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    direction_field[nr][nc] = d
                    q.append((nr, nc))
                    
        return direction_field

    def calculate_initial_solution(self):
        """
        main3.py (経路色付け貪欲法) を実行し、SAの初期解を生成する。
        (V=K を達成できる盤面, 色数C, ルール を返す)
        """
        rules = {} # (c, q) -> (A, S, D)
        visited_cells_map = {} # (i, j) -> c_new
        current_color_id = 0
        
        initial_grid = [[-1] * self.N for _ in range(self.N)] # -1: 未訪問
        
        current_i, current_j = self.targets[0]
        current_q = 0 # 状態0 = 「target_1 を目指す」
        visited_count = 1 
        
        # スタート地点の色割り当て
        visited_cells_map[(current_i, current_j)] = current_color_id
        initial_grid[current_i][current_j] = current_color_id
        current_color_id += 1
        
        # Tステップシミュレーション (main3.py と同じ)
        for step in range(self.T):
            
            # 1. 現在地の色 (c) を決定
            if (current_i, current_j) not in visited_cells_map:
                visited_cells_map[(current_i, current_j)] = current_color_id
                initial_grid[current_i][current_j] = current_color_id
                current_color_id += 1
            
            c = visited_cells_map[(current_i, current_j)]
            q = current_q
            
            if q == self.K - 1: # 全目的地に到達済み
                if (c, q) not in rules:
                    rules[(c, q)] = (c, q, 'S')
                break # シミュレーション終了
            
            # 2. ルール (A, S, D) の決定 (main3.py と同じ)
            if (c, q) not in rules:
                target_pos = self.targets[q + 1]
                if (current_i, current_j) == target_pos:
                    A = c
                    S = q + 1
                    D = self.direction_fields[q + 1][current_i][current_j]
                else:
                    A = c
                    S = q
                    D = self.direction_fields[q][current_i][current_j]
                rules[(c, q)] = (A, S, D)
            
            A, S, D = rules[(c, q)]
            current_q = S
            
            # 3. 移動 (main3.py と同じ)
            if self.can_move(current_i, current_j, D):
                di, dj = self.DIJ[D]
                current_i += di
                current_j += dj
                
            # 4. V カウント (main3.py バグ修正版)
            if visited_count < self.K:
                next_target_index = visited_count
                if (current_i, current_j) == self.targets[next_target_index]:
                    visited_count += 1
        
        # 5. 未訪問マス (-1) を色 0 (スタート地点の色) に割り当てる
        # (色マージの対象にするため)
        for r in range(self.N):
            for c_col in range(self.N):
                if initial_grid[r][c_col] == -1:
                    initial_grid[r][c_col] = 0
                    
        # 6. (重要) 初期解の色数 C0 と V0 を確定
        C0 = current_color_id
        V0 = visited_count
        
        return initial_grid, rules, C0, V0

    def generate_rules_sa(self, grid, C_max):
        """
        SA中: 現在の盤面 s (grid) に基づき、遷移規則 (A, S, D) を生成する。
        (main4.py と同じ、多数決ロジック)
        """
        rules = {}
        for q in range(self.K): # q = 0 .. K-1
            
            # (q == K-1 の場合: 全目的地に到着済み)
            if q == self.K - 1:
                # C_max までの全色に対してルールを定義
                for c in range(C_max):
                    rules[(c, q)] = (c, q, 'S')
                continue

            # (q < K-1 の場合: target_{q+1} を目指す)
            target_pos = self.targets[q + 1]
            
            # 色ごとにマスをグループ化
            cells_by_color = [[] for _ in range(C_max)]
            for r in range(self.N):
                for c_col in range(self.N):
                    color = grid[r][c_col]
                    cells_by_color[color].append((r, c_col))

            for c in range(C_max): # c = 0 .. C_max-1
                cells_with_color_c = cells_by_color[c]
                if not cells_with_color_c:
                    # この色が盤面に存在しない場合 (マージされた後など)
                    rules[(c, q)] = (c, q, 'S') # (暫定: 停止)
                    continue

                is_target_present = False
                direction_at_target = 'S'
                votes_D_stay = collections.Counter()
                
                for (i, j) in cells_with_color_c:
                    if (i, j) == target_pos:
                        is_target_present = True
                        direction_at_target = self.direction_fields[q + 1][i][j]
                    else:
                        votes_D_stay[self.direction_fields[q][i][j]] += 1
                
                if is_target_present:
                    A = c
                    S = q + 1
                    D = direction_at_target
                else:
                    A = c
                    S = q
                    if not votes_D_stay:
                        D = 'S'
                    else:
                        D = votes_D_stay.most_common(1)[0][0]
                
                rules[(c, q)] = (A, S, D)
                
        return rules

    def simulate_sa(self, rules, grid):
        """
        SA中: 生成されたルールと現在の盤面に基づき、シミュレーションを実行する。
        (main4.py と同じ)
        """
        # シミュレーションは盤面のコピーで行う
        sim_grid = [row[:] for row in grid]
        
        current_i, current_j = self.targets[0]
        current_q = 0 
        visited_count = 1 
        
        for step in range(self.T):
            c = sim_grid[current_i][current_j] 
            q = current_q
            
            if (c, q) not in rules:
                break 
                
            A, S, D = rules[(c, q)]
            
            sim_grid[current_i][current_j] = A
            current_q = S
            
            if self.can_move(current_i, current_j, D):
                di, dj = self.DIJ[D]
                current_i += di
                current_j += dj
            
            if visited_count < self.K:
                next_target_index = visited_count
                if (current_i, current_j) == self.targets[next_target_index]:
                    visited_count += 1
            
            if visited_count == self.K:
                return visited_count
        
        return visited_count

    def calculate_energy_sa(self, V, grid):
        """
        SAのエネルギー(最小化対象)を計算する。
        V=K なら C+Q、 未達成ならペナルティ。
        """
        if V == self.K:
            # V=K の場合、エネルギーは C+Q
            # (grid に存在するユニークな色数を数える)
            unique_colors = set()
            for row in grid:
                unique_colors.update(row)
            C = len(unique_colors)
            return C + self.Q
        else:
            # V < K の場合、ペナルティ
            return 2 * (self.N**4) + (self.K - V) * (self.N**2)

    def output_solution(self, grid_raw, rules_M_le_T, V):
        """
        最終的な解の出力と、スコアの stderr への出力を行う。
        (M <= T のルールセットを受け取るよう修正)
        """
        
        # --- 1. スコア計算と stderr への出力 ---
        # (エネルギー計算は V と grid だけで完結する)
        final_score = self.calculate_energy_sa(V, grid_raw)
        print(final_score, file=sys.stderr)

        # --- 2. 回答を 標準出力 (stdout) へ出力 ---
        
        # C (色数) は 1 から C (ユニーク数) にマッピングし直す
        unique_colors = set()
        for row in grid_raw:
            unique_colors.update(row)
        C_mapped = len(unique_colors)
        
        color_map = {old_c: new_c for new_c, old_c in enumerate(unique_colors)}
        
        mapped_grid = [[color_map[c] for c in row] for row in grid_raw]
        mapped_rules = {}
        
        # M <= T のルールセットをマッピング
        for (c_old, q), (A_old, S, D) in rules_M_le_T.items():
            # (c_old や A_old がマージされて unique_colors にない、
            #  という可能性は、シミュレーションで使われた色なら
            #  ありえないはずだが、安全のためチェック)
            if c_old in color_map and A_old in color_map:
                mapped_rules[(color_map[c_old], q)] = (color_map[A_old], S, D)
            elif c_old in color_map:
                # A_old (塗り替え後の色) が盤面に存在しない？
                # (A=c 固定なので、基本的には c_old == A_old のはず)
                # (万が一、A != c のルールが残っていた場合)
                mapped_rules[(color_map[c_old], q)] = (color_map[c_old], S, D) # A=c で代用

        M = len(mapped_rules)
        Q = self.Q

        print(C_mapped, Q, M)
        
        # 初期盤面
        for row in mapped_grid:
            print(' '.join(map(str, row)))
            
        # ルール
        for (c, q), (A, S, D) in mapped_rules.items():
            print(c, q, A, S, D)

    def create_neighbor_sa(self, grid, C_max):
        """
        SA v6 の近傍操作 (マージ / スワップ / スプリット)
        C_max: 初期解の色数 (これ以上は増やさない)
        """
        new_grid = [row[:] for row in grid] # Deep copy
        
        # 盤面に存在する色と、その色のマス座標リスト
        colors_on_grid = collections.defaultdict(list)
        for r in range(self.N):
            for c in range(self.N):
                colors_on_grid[grid[r][c]].append((r, c))
        
        current_colors = list(colors_on_grid.keys())
        current_C = len(current_colors)

        op_type = random.random()
        
        if op_type < 0.4 and current_C > 1:
            # --- A. 色のマージ (C-1) ---
            c1, c2 = random.sample(current_colors, 2)
            for (r, c) in colors_on_grid[c1]:
                new_grid[r][c] = c2
        
        elif op_type < 0.8:
            # --- B. 色の付け替え (Cは不変) ---
            if not current_colors: return new_grid # (ありえないが念のため)
            c1 = random.choice(current_colors)
            c2 = random.choice(current_colors)
            if c1 == c2 or not colors_on_grid[c1]:
                return new_grid # 変更なし
                
            (r, c) = random.choice(colors_on_grid[c1])
            new_grid[r][c] = c2
            
        else:
            # --- C. 色の分離 (C+1) ---
            if current_C >= C_max:
                return new_grid # 上限
                
            # C_max までの範囲で、現在使われていない色を探す
            available_new_colors = []
            current_colors_set = set(current_colors)
            for c_new in range(C_max):
                if c_new not in current_colors_set:
                    available_new_colors.append(c_new)
            
            if not available_new_colors:
                return new_grid # 分離不可
            
            c_new = random.choice(available_new_colors)
            c1 = random.choice(current_colors)
            if not colors_on_grid[c1]:
                return new_grid
                
            (r, c) = random.choice(colors_on_grid[c1])
            new_grid[r][c] = c_new

        return new_grid

    def run_final_simulation_and_remap(self, grid_raw, C_max_raw):
        """
        SAのベスト解 (grid_raw) を受け取り、
        1. 色を 0..C-1 にリマップ
        2. 評価用ルール (M > T) を生成
        3. Tステップシミュレーションを *実行* し、
           実際に遭遇したルール (M <= T) のみ収集
        4. (mapped_grid, rules_M_le_T, V) を返す
        """
        
        # --- 1. 色を 0..C-1 にリマップ ---
        unique_colors = set()
        for row in grid_raw:
            unique_colors.update(row)
        C_mapped = len(unique_colors)
        
        color_map = {old_c: new_c for new_c, old_c in enumerate(unique_colors)}
        mapped_grid = [[color_map[c] for c in row] for row in grid_raw]
        
        # --- 2. 評価用ルール (M > T) を生成 ---
        # (リマップ後の盤面と C_mapped を使う)
        rules_eval = self.generate_rules_sa(mapped_grid, C_mapped)
        
        # --- 3. Tステップシミュレーション (M <= T ルール収集) ---
        output_rules_M_le_T = {} # 実際に出力するルール
        
        sim_grid = [row[:] for row in mapped_grid] # シミュレーション用グリッド
        
        current_i, current_j = self.targets[0]
        current_q = 0 
        visited_count = 1 
        
        for step in range(self.T):
            c = sim_grid[current_i][current_j]
            q = current_q
            
            if q == self.K - 1: # 完了
                if (c, q) not in output_rules_M_le_T:
                    if (c, q) in rules_eval: # 念のため
                        output_rules_M_le_T[(c, q)] = rules_eval[(c, q)]
                    else:
                        output_rules_M_le_T[(c, q)] = (c, q, 'S')
                break
                
            if (c, q) not in rules_eval:
                # 多数決ルールがない (C_max_raw > C_mapped の場合？)
                # (ありえないはずだが、安全のため停止)
                break
                
            # (c, q) のルールを (M <= T) セットに追加
            if (c, q) not in output_rules_M_le_T:
                output_rules_M_le_T[(c, q)] = rules_eval[(c, q)]
            
            A, S, D = output_rules_M_le_T[(c, q)]
            
            sim_grid[current_i][current_j] = A
            current_q = S
            
            if self.can_move(current_i, current_j, D):
                di, dj = self.DIJ[D]
                current_i += di
                current_j += dj
            
            if visited_count < self.K:
                next_target_index = visited_count
                if (current_i, current_j) == self.targets[next_target_index]:
                    visited_count += 1
        
        return mapped_grid, output_rules_M_le_T, visited_count

    def solve(self):
        """
        メイン処理:
        1. 初期解 (main3.py, M<=T) を生成
        2. 残り時間で SA (v6) を実行
        3. (M <= T) ルールを再生成して出力
        """
        
        # --- 1. 初期解の生成 (M <= T) ---
        initial_grid, initial_rules_M_le_T, initial_C, initial_V = self.calculate_initial_solution()
        
        # --- SA 初期設定 ---
        current_grid = initial_grid
        current_energy = self.calculate_energy_sa(initial_V, current_grid) 
        current_V = initial_V
        
        best_grid_raw = current_grid # (未マッピングの grid)
        best_rules_M_le_T = initial_rules_M_le_T # (M <= T のルール)
        best_energy = current_energy
        best_V = initial_V
        
        C_max = initial_C # 色分離の上限

        T_start = 10.0
        T_end = 0.1
        iteration = 0
        
        # --- 2. SA メインループ (残り時間) ---
        while True:
            iteration += 1
            if iteration % 100 == 0: # 100回に1回、時間チェック
                now = time.time()
                if now - self.START_TIME > self.TIME_LIMIT:
                    break
            
            time_elapsed = time.time() - self.START_TIME
            time_remaining_ratio = (self.TIME_LIMIT - time_elapsed) / self.TIME_LIMIT
            if time_remaining_ratio <= 0:
                 break
            
            temp = T_end + (T_start - T_end) * time_remaining_ratio
            if temp <= 0: temp = T_end
            
            # 近傍解の生成 (v6)
            new_grid = self.create_neighbor_sa(current_grid, C_max)
            
            # 近傍解の評価 (M > T ルールを使用)
            new_rules_eval = self.generate_rules_sa(new_grid, C_max) 
            new_V = self.simulate_sa(new_rules_eval, new_grid)
            new_energy = self.calculate_energy_sa(new_V, new_grid)
            
            # --- SA 遷移判定 ---
            delta_energy = new_energy - current_energy
            
            if delta_energy <= 0 or random.random() < math.exp(-delta_energy / temp):
                current_grid = new_grid
                current_energy = new_energy
                current_V = new_V
                
                # ベスト解の更新
                if current_energy < best_energy:
                    best_grid_raw = new_grid
                    best_energy = new_energy
                    best_V = new_V
                    # (重要) この時点では M <= T のルールは未生成
                    best_rules_M_le_T = None 
                    
        
        # --- 3. 最終解の出力 (M <= T ルールを保証) ---
        
        final_grid = None
        final_rules = None
        final_V = 0
        
        if best_rules_M_le_T is not None:
            # --- 初期解が最良だった場合 ---
            # (initial_grid は 0..C0-1 の色を使っている)
            final_grid = best_grid_raw
            final_rules = best_rules_M_le_T
            final_V = best_V
        
        else:
            # --- SAが改善解 (best_grid_raw) を見つけた場合 ---
            # (M <= T のルールを再生成する必要がある)
            final_grid, final_rules, final_V = self.run_final_simulation_and_remap(
                best_grid_raw, C_max
            )

        self.output_solution(final_grid, final_rules, final_V)


if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()