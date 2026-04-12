import sys
import collections

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1.5: 経路色付け貪欲法 + スコア出力)

    コンセプト (Step 1.5):
    - Q (状態数) = K
    - C (色数) = シミュレーションで「実際に通ったマス」の数
    - 事前計算: 全ての目的地ペアへの最適移動方向をBFSで計算。

    追加機能 (run.sh 連携):
    - シミュレーションを実行し、訪問できた目的地 V を正確にカウント。
    - 最終的な絶対スコアを計算し、標準エラー出力 (stderr) に出力する。
    """

    def __init__(self):
        """
        入力の読み込みと初期化
        """
        self.N, self.K, self.T = map(int, sys.stdin.readline().split())
        self.v_walls = [sys.stdin.readline().strip() for _ in range(self.N)]
        self.h_walls = [sys.stdin.readline().strip() for _ in range(self.N - 1)]
        self.targets = [tuple(map(int, sys.stdin.readline().split())) for _ in range(self.K)]

        # 移動方向 (U, D, L, R)
        self.DIJ = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1), 'S': (0, 0)}
        self.DIR_CHARS = "UDLRS"

        # Q (状態数) の設定
        self.Q = self.K 
        self.C = 0 
        
        # 最終的な訪問目的地数を格納
        self.V = 0 

        # --- アルゴリズム核心部 (事前計算) ---
        self.direction_fields = []
        for k in range(self.K - 1):
            self.direction_fields.append(self.calculate_direction_field(self.targets[k + 1]))

    def can_move(self, i, j, d):
        """
        マス(i, j)から方向dに移動可能か（壁がないか）を判定する
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
        全マスからの「最適移動方向」のフィールドを計算する。
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

    def solve(self):
        """
        シミュレーションを実行し、
        「通ったマス」にのみ色を割り当て、ルールを生成して出力する。
        最後にスコアを stderr に出力する。
        """
        
        rules = {} 
        visited_cells_map = {} 
        current_color_id = 0 
        
        current_i, current_j = self.targets[0]
        current_q = 0 # 状態0 = 「target_1 を目指す」
        
        # --- スコア計算用 ---
        # visited_count は「訪問済みの目的地の数」
        # スタート地点 (target_0) にいるため、初期値は 1
        visited_count = 1 
        
        # Tステップシミュレーション
        for step in range(self.T):
            
            # --- 1.5 核心部: 現在地の「色」を動的に決定 ---
            current_pos = (current_i, current_j)
            if current_pos not in visited_cells_map:
                visited_cells_map[current_pos] = current_color_id
                current_color_id += 1
            
            c = visited_cells_map[current_pos] 
            q = current_q 
            
            # --- 状態 K-1 (最後の目的地に到着済み) の処理 ---
            if q == self.K - 1:
                if (c, q) not in rules:
                    rules[(c, q)] = (c, q, 'S')
                # 既に全目的地に到達しているので、ループを抜ける
                break 

            # --- ルール決定 ---
            if (c, q) not in rules:
                target_pos = self.targets[q + 1] # 現在目指している目的地

                if (current_i, current_j) == target_pos:
                    # --- 次の目的地に到達した ---
                    A = c 
                    S = q + 1 
                    
                    if S == self.K - 1:
                        # 最後の目的地 (target_{K-1}) に到着した
                        D = 'S'
                    else:
                        # まだ中間の目的地
                        D = self.direction_fields[S][current_i][current_j]
                
                else:
                    # --- 目的地へ移動中 ---
                    A = c 
                    S = q 
                    D = self.direction_fields[q][current_i][current_j]
                
                rules[(c, q)] = (A, S, D)
            
            # 決定したルールを取得
            A, S, D = rules[(c, q)]

            # 状態更新
            current_q = S
            
            # 移動
            if self.can_move(current_i, current_j, D):
                di, dj = self.DIJ[D]
                current_i += di
                current_j += dj
                
            # --- スコア計算用: 訪問済み目的地数の更新 (バグ修正) ---
            # 「最後のターンに着く場合」を考慮し、移動*後*の位置で判定する

            # (旧ロジック: q基準)
            # if current_q + 1 > visited_count:
            #     visited_count = current_q + 1
            # (↑ Tターン目に移動して target[K-1] に着いた場合、
            #    q は K-2 のままループが終わり、V が K-1 になっていた)

            # (新ロジック: 位置基準)
            # visited_count は「訪問済みの*数*」
            # (例) V=1 (target_0済) -> 次は target_1 (index 1) を目指す
            # (例) V=K-1 (target_0..K-2済) -> 次は target_{K-1} (index K-1) を目指す
            
            if visited_count < self.K: # まだ全目的地に着いていない
                next_target_index = visited_count
                next_target_pos = self.targets[next_target_index]
                
                if (current_i, current_j) == next_target_pos:
                    # 次の目的地に（移動後に）到達した
                    visited_count += 1
            
            # (補足)
            # K-1個目の目的地 (target[K-2]) に着いた時:
            #   V=K-1, next_target_index=K-1, pos=target[K-1]
            #   -> V=K に更新される
            # K個目の目的地 (target[K-1]) に着いた時:
            #   V=K-1, next_target_index=K-1, pos=target[K-1]
            #   -> V=K に更新される

        # --- ループ終了後の最終訪問数 ---
        # (旧ロジックは削除)
        # Tステップを使い切った場合でも、最後の Vチェック (if current_q + 1 > visited_count)
        # が正しく動作しているため、追加のチェックは不要。
            
        self.V = visited_count
        self.C = current_color_id 

        # --- 1. スコア計算と stderr への出力 ---
        final_score = 0
        if self.V == self.K:
            final_score = self.C + self.Q
        else:
            # V < K の場合 (ペナルティ)
            final_score = 2 * (self.N**4) + (self.K - self.V) * (self.N**2)

        # 【重要】計算した「絶対スコア」を 標準エラー出力 (stderr) に *だけ* 出力する
        print(final_score, file=sys.stderr)

        # --- 2. 回答を 標準出力 (stdout) へ出力 ---
        print(self.C, self.Q, len(rules))
        
        # 初期盤面
        initial_grid = [[0] * self.N for _ in range(self.N)]
        for (i, j), color in visited_cells_map.items():
            initial_grid[i][j] = color
        for row in initial_grid:
            print(' '.join(map(str, row)))
            
        # ルール
        for (c, q), (A, S, D) in rules.items():
            print(c, q, A, S, D)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()