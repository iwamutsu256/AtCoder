import sys
import collections

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1.5: 経路色付け貪欲法)

    コンセプト (Step 1 改良):
    - Q (状態数) = K: 内部状態 q は「次に target_{q+1} を目指している」ことを示す。
    - 事前計算: 全ての目的地ペア (target_k -> target_{k+1}) について、
      target_{k+1} からBFSを行い、全マスからの最適移動方向を計算しておく。

    改良点 (Step 1.5 - むつきさんのご提案):
    - C (色数) = N*N ではなく、シミュレーションで「実際に通ったマス」の数だけにする。
    - 1回のシミュレーションで、通ったマス (i, j) にユニークな色 c_new (0から連番) を割り当て。
    - 通らなかったマスはすべてデフォルト色 (0) にする。
    - スコアは C + Q = (通ったマスの数) + K となり、大幅に改善する。
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
        self.Q = self.K # 状態 0, 1, ..., K-1 (K-1は完了状態)
        # C (色数) は solve メソッド内で動的に決定する
        self.C = 0
        # 現時点で目標地点に到着した数 
        self.V = 0

        # --- アルゴリズム核心部 (事前計算) ---
        # direction_fields[k][i][j] = target_{k+1} へ向かうための (i,j) での最適方向
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
        (内容は GridTuringRobot_Greedy_Optimized.py と同一)
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
        """
        
        # --- シミュレーションによる色割り当て と ルール生成 ---
        rules = {} # (c_new, q) -> (A, S, D) のマッピング
        
        # visited_cells_map[(i, j)] = c_new (新しい色ID)
        visited_cells_map = {} 
        current_color_id = 0 # 次に割り当てる新しい色ID
        
        current_i, current_j = self.targets[0]
        current_q = 0 # 状態0 = 「target_1 を目指す」
        
        # Tステップシミュレーション
        for step in range(self.T):
            
            # --- 1.5 核心部: 現在地の「色」を動的に決定 ---
            current_pos = (current_i, current_j)
            if current_pos not in visited_cells_map:
                # このマスに初めて来た
                visited_cells_map[current_pos] = current_color_id
                current_color_id += 1
            
            c = visited_cells_map[current_pos] # 現在地の色
            q = current_q # 現在の状態
            
            # --- 状態 K-1 (最後の目的地に到着済み) の処理 ---
            if q == self.K - 1:
                # 完了状態 (K-1) になったら、どのマスでも停止(S)するルールを追加
                if (c, q) not in rules:
                    # 色は変えない(A=c), 状態も変えない(S=q), 停止(D='S')
                    rules[(c, q)] = (c, q, 'S')
                    self.V += 1
                break # シミュレーション終了

            # (c, q) のルールが未定義の場合のみ、ルールを決定する
            if (c, q) not in rules:
                target_pos = self.targets[q + 1] # 現在目指している目的地

                if (current_i, current_j) == target_pos:
                    # --- 次の目的地に到達した ---
                    A = c # 色は変えない
                    S = q + 1 # 状態を更新
                    self.V += 1
                    print(step,self.V,current_i,current_j,file=sys.stderr)
                    
                    if S == self.K - 1:
                        # 最後の目的地 (target_{K-1}) に到着した
                        D = 'S'
                    else:
                        # まだ中間の目的地
                        # *次*の方向場 (direction_fields[S]) に従って移動
                        D = self.direction_fields[S][current_i][current_j]
                
                else:
                    # --- 目的地へ移動中 ---
                    A = c # 色は変えない
                    S = q # 状態はそのまま
                    # *今*の方向場 (direction_fields[q]) に従って移動
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
            # print(step,current_i,current_j,file=sys.stderr)
        else:
            # --- 1.5 核心部: 現在地の「色」を動的に決定 ---
            current_pos = (current_i, current_j)
            q = current_q
            if current_pos == self.targets[q+1]:
                self.V += 1
                print(step+1,self.V,current_i,current_j,file=sys.stderr)
            print(q,self.K-1,file=sys.stderr)
            if q == self.K - 1:
                # 完了状態 (K-1) になったら、どのマスでも停止(S)するルールを追加
                if (c, q) not in rules:
                    # 色は変えない(A=c), 状態も変えない(S=q), 停止(D='S')
                    rules[(c, q)] = (c, q, 'S')
                    self.V += 1



        # --- 最終的な C と 初期盤面の生成 ---
        self.C = current_color_id # 実際に使った色の総数
        
        # デフォルト色 0 で初期化
        initial_grid = [[0] * self.N for _ in range(self.N)]
        
        # 訪問したマスの色を設定
        for (i, j), color in visited_cells_map.items():
            initial_grid[i][j] = color

        # --- 出力 ---
        print(self.C, self.Q, len(rules))
        
        # 初期盤面
        for row in initial_grid:
            print(' '.join(map(str, row)))
            
        # ルール
        for (c, q), (A, S, D) in rules.items():
            print(c, q, A, S, D)
        
        # スコアを標準エラー出力に出力
        final_score = 0
        if self.V == self.K:
            final_score = self.C + self.Q
        else:
            final_score = 2*(self.N**4) + (self.K-self.V) * (self.N**2)
        print(final_score,self.V,self.K, file=sys.stderr)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()