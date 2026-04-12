import sys
import collections

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1: 貪欲法)

    コンセプト:
    - C (色数) = N*N: 各マス(i, j)に固有の色 c = i * N + j を割り当てる。
    - Q (状態数) = K: 内部状態 q = k は「次に target_{k+1} を目指している」ことを示す。
    - 事前計算: 全ての目的地ペア (target_k -> target_{k+1}) について、
      target_{k+1} からBFSを行い、全マスからの最適移動方向を計算しておく。
    - ルール生成: 実際にロボットをシミュレーションし、遭遇した (c, q) の組
      に対する遷移ルールのみを生成する。
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

        # C (色数) と Q (状態数) の設定
        self.C = self.N * self.N
        self.Q = self.K

        # --- アルゴリズム核心部 (事前計算) ---
        # direction_fields[k][i][j] = target_{k+1} へ向かうための (i,j) での最適方向
        self.direction_fields = []
        for k in range(self.K - 1):
            # target_{k+1} からBFSして方向場を計算
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

    def get_color(self, i, j):
        """
        座標(i, j)から色cを取得する
        """
        return i * self.N + j

    def calculate_direction_field(self, target_pos):
        """
        指定された目的地 target_pos からBFSを行い、
        全マスからの「最適移動方向」のフィールドを計算する。

        Args:
            target_pos (tuple): 目的地の座標 (tr, tc)

        Returns:
            list[list[str]]: (N x N) の方向フィールド ('U', 'D', 'L', 'R', 'S')
        """
        tr, tc = target_pos
        dist = [[-1] * self.N for _ in range(self.N)]
        direction_field = [['S'] * self.N for _ in range(self.N)]
        
        q = collections.deque()
        q.append(target_pos)
        dist[tr][tc] = 0

        while q:
            r, c = q.popleft()

            # (r, c) に 'S' (Stay) 以外の方向で到達したマスを探す
            for d in self.DIR_CHARS:
                if d == 'S': continue
                
                # 逆方向の移動を試す
                di, dj = self.DIJ[d]
                nr, nc = r - di, c - dj

                # グリッド外か？
                if not (0 <= nr < self.N and 0 <= nc < self.N):
                    continue
                
                # (nr, nc) -> (r, c) への移動は可能か？
                if not self.can_move(nr, nc, d):
                    continue
                    
                # (nr, nc) が未訪問か？
                if dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    direction_field[nr][nc] = d # (nr, nc) からは d 方向に進むべき
                    q.append((nr, nc))
                    
        return direction_field

    def solve(self):
        """
        シミュレーションを実行し、ルールを生成して出力する。
        """
        
        # --- 初期盤面の生成 ---
        # s[i][j] = i * N + j
        initial_grid = [[self.get_color(i, j) for j in range(self.N)] for i in range(self.N)]

        # --- シミュレーションによるルール生成 ---
        rules = {} # (c, q) -> (A, S, D) のマッピング
        
        current_i, current_j = self.targets[0]
        current_q = 0 # 状態0 = 「target_1 を目指す」
        
        visited_targets = 0 # (V=K達成確認用。このロジックでは不要だが念のため)
        
        if (current_i, current_j) == self.targets[0]:
            visited_targets = 1

        # Tステップシミュレーション
        for step in range(self.T):
            if current_q == self.K - 1:
                # 既に最後の目的地に到達している (q = K-1)
                # 念のため、停止ルールを追加
                c = self.get_color(current_i, current_j)
                if (c, current_q) not in rules:
                    rules[(c, current_q)] = (c, current_q, 'S')
                break # シミュレーション終了

            c = self.get_color(current_i, current_j)
            q = current_q
            
            # (c, q) のルールが未定義の場合のみ、ルールを決定する
            if (c, q) not in rules:
                target_pos = self.targets[q + 1]

                if (current_i, current_j) == target_pos:
                    # --- 次の目的地に到達した ---
                    A = c # 色は変えない
                    S = q + 1 # 状態を更新
                    D = 'S' # 移動しない
                else:
                    # --- 目的地へ移動中 ---
                    A = c # 色は変えない
                    S = q # 状態はそのまま
                    D = self.direction_fields[q][current_i][current_j] # 事前計算した最適方向
                
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
                
            # (デバッグ用) 目的地到達の確認
            if current_q == visited_targets and (current_i, current_j) == self.targets[current_q]:
                visited_targets += 1
                if visited_targets == self.K:
                    # 全て訪問完了。
                    # current_q は K-1 になっているはず。
                    # 次のループの冒頭でbreakする。
                    pass

        # --- 出力 ---
        print(self.C, self.Q, len(rules))
        
        # 初期盤面
        for row in initial_grid:
            print(' '.join(map(str, row)))
            
        # ルール
        for (c, q), (A, S, D) in rules.items():
            print(c, q, A, S, D)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()