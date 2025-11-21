import sys
import collections
import time
import heapq

# 標準入力の再帰深度を増やす
sys.setrecursionlimit(200010)

class GridTuringRobotSolver:
    """
    AHC問題「A - Grid Turing Robot」の解法クラス (Step 1.7: 経路再利用Dijkstra法)

    コンセプト (v7):
    - Q (状態数) = K (固定)
    - C (色数) = 動的に決定
    - main3.py (経路色付け) の経路探索を、BFS (最短) から
      カスタムDijkstra法 (既存セル再利用) に変更する。
    - Dijkstraコスト:
        - 既存セルへの移動: 1
        - 新規セルへの移動: 1001 (N*N=400より十分大きく、ステップ数1も考慮)
    - これにより、Dijkstraは「新規セル数を最小に、次にステップ数を最小に」
      する経路 (既存セルを最大限再利用する経路) を見つける。
    - Tステップを超えない限り、Cが main3 よりも削減されることが期待される。
    """

    def __init__(self):
        """
        入力の読み込みと初期化 (main5.py とほぼ同じ)
        """
        self.START_TIME = time.time()
        self.TIME_LIMIT = 1.8 # 2.0秒制限

        self.N, self.K, self.T = map(int, sys.stdin.readline().split())
        self.v_walls = [sys.stdin.readline().strip() for _ in range(self.N)]
        self.h_walls = [sys.stdin.readline().strip() for _ in range(self.N - 1)]
        self.targets = [tuple(map(int, sys.stdin.readline().split())) for _ in range(self.K)]

        self.DIJ = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1), 'S': (0, 0)}
        self.DIR_CHARS = "UDLRS"
        self.Q = self.K
        
        # --- v7 では direction_fields (BFS) は不要 ---
        # self.direction_fields = [] 

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

    def find_path_dijkstra(self, start_pos, goal_pos, global_visited_cells):
        """
        v7 核心部: カスタムDijkstra法による経路探索
        start_pos から goal_pos までの「既存セル再利用」経路を見つける。

        Args:
            start_pos (tuple): スタート座標 (sr, sc)
            goal_pos (tuple): ゴール座標 (gr, gc)
            global_visited_cells (set): これまでに訪問した全マスのセット

        Returns:
            list[tuple]: 経路上の座標リスト (start除く, goal含む)
            int: この経路の総ステップ数
        """
        
        # コスト（新規=1001, 既存=1）
        COST_NEW = 1001 # (N*N=400 より十分大きい値 + ステップ数 1)
        COST_EXISTING = 1
        
        sr, sc = start_pos
        gr, gc = goal_pos
        
        # dist[r][c] = (最小コスト, 最小ステップ数)
        dist = [[(float('inf'), float('inf'))] * self.N for _ in range(self.N)]
        
        # prev[r][c] = (pr, pc) (経路復元用)
        prev = [[None] * self.N for _ in range(self.N)]
        
        # 優先度キュー: ( (コスト, ステップ数), (r, c) )
        pq = [( (0, 0), start_pos )]
        dist[sr][sc] = (0, 0)

        path_found = False
        
        while pq:
            (current_cost, current_steps), (r, c) = heapq.heappop(pq)

            # ゴールに到達
            if (r, c) == goal_pos:
                path_found = True
                break
                
            # 既に古い情報（より良い経路が見つかっている）
            if (current_cost, current_steps) > dist[r][c]:
                continue
            
            # 4方向 (U, D, L, R) に移動
            for d in self.DIR_CHARS:
                if d == 'S': continue
                
                if not self.can_move(r, c, d):
                    continue
                    
                di, dj = self.DIJ[d]
                nr, nc = r + di, c + dj
                
                # (nr, nc) への移動コストを計算
                edge_cost = 0
                if (nr, nc) in global_visited_cells:
                    edge_cost = COST_EXISTING
                else:
                    edge_cost = COST_NEW
                
                new_cost = current_cost + edge_cost
                new_steps = current_steps + 1
                
                if (new_cost, new_steps) < dist[nr][nc]:
                    dist[nr][nc] = (new_cost, new_steps)
                    prev[nr][nc] = (r, c)
                    heapq.heappush(pq, ( (new_cost, new_steps), (nr, nc) ) )

        # --- 経路復元 ---
        path = []
        if not path_found:
            # (ありえないはずだが、念のため)
            return [], 0 
            
        curr = goal_pos
        while curr != start_pos:
            path.append(curr)
            curr = prev[curr[0]][curr[1]]
        
        path.reverse() # goal -> start を start -> goal に
        
        total_steps = dist[gr][gc][1]
        
        return path, total_steps

    def solve(self):
        """
        メイン処理:
        1. Dijkstra法で K-1 本の経路を逐次決定
        2. Tステップチェック
        3. 色付け (main3 と同じ)
        4. 出力 (main3 と同じ)
        """
        
        global_visited_cells = set() # これまでに通った全マスのセット
        global_total_steps = 0
        all_paths = [] # K-1 本の経路 (座標リスト) を格納
        
        # スタート地点を訪問済みに
        global_visited_cells.add(self.targets[0])
        
        # --- 1. Dijkstra法で K-1 本の経路を逐次決定 ---
        for k in range(self.K - 1):
            start_pos = self.targets[k]
            goal_pos = self.targets[k + 1]
            
            # v7 核心部
            path_k, steps_k = self.find_path_dijkstra(
                start_pos, goal_pos, global_visited_cells
            )
            
            if not path_k:
                # 経路が見つからない (通常ありえない)
                global_total_steps = float('inf') 
                break
                
            all_paths.append(path_k)
            global_total_steps += steps_k
            
            # この経路で通った *新規* マスを global_visited_cells に追加
            for pos in path_k:
                global_visited_cells.add(pos)
        
        # --- 2. Tステップチェック ---
        V = 0
        if global_total_steps <= self.T:
            V = self.K
        else:
            # Tを超えた場合、V=K ではない (ペナルティ)
            # (途中までの V を計算する必要があるが、
            #  この貪欲法は V=K 達成が前提なので、
            #  T超えは「失敗」として扱う)
            
            # (厳密に V を計算するロジック)
            V = 1 # target_0
            steps_so_far = 0
            for k in range(self.K - 1):
                steps_k = len(all_paths[k]) # path_k のステップ数
                if steps_so_far + steps_k <= self.T:
                    steps_so_far += steps_k
                    V += 1
                else:
                    break # T超え

        # --- 3. 色付け と ルール生成 (main3 と同じ) ---
        # (ただし、経路はDijkstraで決定済みのものを使う)
        
        rules = {} # (c_new, q) -> (A, S, D)
        visited_cells_map = {} # (i, j) -> c_new
        current_color_id = 0
        
        current_q = 0 # 状態0 = 「target_1 を目指す」
        
        # Tステップシミュレーション (ただし経路は固定)
        current_pos = self.targets[0]
        
        # スタート地点の色割り当て
        visited_cells_map[current_pos] = current_color_id
        current_color_id += 1
        
        # K-1 本の経路を順にたどる
        for k in range(self.K - 1):
            path_k = all_paths[k]
            q = k # 現在の状態 q=k (target_{k+1} を目指す)
            
            if not path_k: continue # (念のため)

            # 経路 (path_k) を1ステップずつ進む
            for step_idx in range(len(path_k)):
                pos = path_k[step_idx]
                
                # --- 色の割り当て ---
                if pos not in visited_cells_map:
                    visited_cells_map[pos] = current_color_id
                    current_color_id += 1
                
                c = visited_cells_map[pos]
                
                # --- ルールの決定 ---
                if (c, q) not in rules:
                    A = c # 色は変えない
                    
                    is_last_step = (step_idx == len(path_k) - 1)
                    
                    if is_last_step:
                        # --- この経路のゴール (target_{k+1}) に到達 ---
                        S = q + 1 # 状態を更新
                        
                        if S == self.K - 1:
                            # 最後の目的地 (target_{K-1}) だった
                            D = 'S'
                        else:
                            # まだ中間の目的地
                            # *次*の経路 (all_paths[k+1]) の *最初の一歩* の方向
                            next_path = all_paths[k+1]
                            if not next_path:
                                D = 'S' # 次の経路がない？
                            else:
                                next_pos = next_path[0]
                                if next_pos[0] < pos[0]: D = 'U'
                                elif next_pos[0] > pos[0]: D = 'D'
                                elif next_pos[1] < pos[1]: D = 'L'
                                elif next_pos[1] > pos[1]: D = 'R'
                                else: D = 'S' # (ありえない: start == goal)
                    else:
                        # --- 経路の移動中 ---
                        S = q # 状態はそのまま
                        # *次*のマス (path_k[step_idx + 1]) への方向
                        next_pos = path_k[step_idx + 1]
                        if next_pos[0] < pos[0]: D = 'U'
                        elif next_pos[0] > pos[0]: D = 'D'
                        elif next_pos[1] < pos[1]: D = 'L'
                        elif next_pos[1] > pos[1]: D = 'R'
                        else: D = 'S' # (ありえない: 同じマス)
                    
                    rules[(c, q)] = (A, S, D)

        # --- 4. 出力 ---
        
        # 最終的な C
        self.C = current_color_id
        self.V = V # Tステップチェックに基づいた V
        
        # 初期盤面
        initial_grid = [[0] * self.N for _ in range(self.N)]
        for (i, j), color in visited_cells_map.items():
            initial_grid[i][j] = color

        # --- スコア計算 (stderr) ---
        final_score = 0
        if self.V == self.K:
            final_score = self.C + self.Q
        else:
            final_score = 2 * (self.N**4) + (self.K - self.V) * (self.N**2)
        
        print(final_score, file=sys.stderr)

        # --- 回答 (stdout) ---
        print(self.C, self.Q, len(rules))
        for row in initial_grid:
            print(' '.join(map(str, row)))
        for (c, q), (A, S, D) in rules.items():
            print(c, q, A, S, D)

if __name__ == "__main__":
    solver = GridTuringRobotSolver()
    solver.solve()