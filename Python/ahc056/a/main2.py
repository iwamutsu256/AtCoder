import sys
import collections

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1 改良版)

    コンセプト (Step 1):
    - C (色数) = N*N: 各マス(i, j)に固有の色 c = i * N + j を割り当てる。
    - Q (状態数) = K: 内部状態 q は「次に target_{q+1} を目指している」ことを示す (q=0..K-2)。
                     q = K-1 は「完了」状態。
    - 事前計算: 全ての目的地ペア (target_k -> target_{k+1}) について、
      target_{k+1} からBFSを行い、全マスからの最適移動方向を計算しておく。

    改良点 (むつきさんのご指摘):
    - 目的地到着時の「停止(D='S')」を廃止。
    - 目的地 (target_{q+1}) に到着したマス (色c) で状態 (q) だった場合、
      ルール (c, q) は、状態を S = q+1 に更新し、*かつ*、
      D = (次の目的地 target_{q+2} への最適方向) に設定する。
    - これにより、ターン消費なしで次の目的地へ向かい始める。
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
        self.Q = self.K # 状態 0, 1, ..., K-1 (K-1は完了状態)

        # --- アルゴリズム核心部 (事前計算) ---
        # direction_fields[k][i][j] = target_{k+1} へ向かうための (i,j) での最適方向
        # k は 0 から K-2 まで (K-1個のフィールド)
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
        (目的地到着時のターン消費をなくすよう改良)
        """
        
        # --- 初期盤面の生成 ---
        # s[i][j] = i * N + j
        initial_grid = [[self.get_color(i, j) for j in range(self.N)] for i in range(self.N)]

        # --- シミュレーションによるルール生成 ---
        rules = {} # (c, q) -> (A, S, D) のマッピング
        
        current_i, current_j = self.targets[0]
        current_q = 0 # 状態0 = 「target_1 を目指す」
        
        # Tステップシミュレーション
        for step in range(self.T):
            # --- 状態 K-1 (最後の目的地に到着済み) の処理 ---
            if current_q == self.K - 1:
                c = self.get_color(current_i, current_j)
                q = self.K - 1
                # 完了状態 (K-1) になったら、どのマスでも停止(S)するルールを追加
                if (c, q) not in rules:
                    rules[(c, q)] = (c, q, 'S')
                break # シミュレーション終了

            # 現在の色と状態
            c = self.get_color(current_i, current_j)
            q = current_q
            
            # (c, q) のルールが未定義の場合のみ、ルールを決定する
            if (c, q) not in rules:
                target_pos = self.targets[q + 1] # 現在目指している目的地

                # --- 核心部: 目的地にジャストで到着したか？ ---
                if (current_i, current_j) == target_pos:
                    # --- 次の目的地に到達した ---
                    A = c # 色は変えない
                    S = q + 1 # 状態を更新
                    
                    if S == self.K - 1:
                        # 最後の目的地 (target_{K-1}) に到着した
                        # 状態は K-1 に更新し、移動は停止(S)する
                        D = 'S'
                    else:
                        # まだ中間の目的地
                        # 状態を S (q+1) に更新し、
                        # *次*の方向場 (direction_fields[S]) に従って移動する
                        D = self.direction_fields[S][current_i][current_j]
                
                else:
                    # --- 目的地へ移動中 ---
                    A = c # 色は変えない
                    S = q # 状態はそのまま
                    # *今*の方向場 (direction_fields[q]) に従って移動する
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