import sys
import math
from collections import deque
import time
import heapq # v6.5/v6.6 のDijkstraは不使用
import random # v8.0: SA と StochasticBFS のために追加

# --- 開発規約: stderr へのスコア出力 ---
def print_score(score):
    """
    開発規約に基づき、最終的な絶対スコアを標準エラー出力に出力します。
    (v6.0 と同一)
    Args:
        score (int): C+Q またはペナルティスコア
    """
    print(score, file=sys.stderr)

# --- グローバル変数 (入力から設定) ---
N = 0
K = 0
T = 0
VWALLS = []
HWALLS = []
TARGETS = []

# --- v8.0: BfsSolver (v6.0) ---
# 決定論的BFS。キャッシュを使い、高速に初期解を生成する。
class BfsSolver:
    """
    壁情報を考慮したBFS（幅優先探索）を実行し、
    「決定論的な」最短経路を計算するクラス。(v6.0 と同一)
    """
    def __init__(self, n, vwalls, hwalls):
        self.N = n
        self.vwalls = vwalls
        self.hwalls = hwalls
        self.moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
        self.cache = {} 

    def solve(self, sr, sc, gr, gc):
        """
        (sr, sc) から (gr, gc) への「決定論的な」最短経路を計算します。(キャッシュ利用)
        """
        start_node = (sr, sc)
        goal_node = (gr, gc)
        
        if (start_node, goal_node) in self.cache:
            return self.cache[(start_node, goal_node)]

        q = deque([(sr, sc)])
        prev = [[None] * self.N for _ in range(self.N)]
        prev[sr][sc] = (-1, -1, 'S')
        
        found = False
        while q:
            r, c = q.popleft()
            if r == gr and c == gc:
                found = True
                break
            
            # v6.0: この moves の順序が決定論的
            for dr, dc, move in self.moves:
                nr, nc = r + dr, c + dc
                
                if not (0 <= nr < self.N and 0 <= nc < self.N): continue
                if move == 'U' and self.hwalls[r-1][c] == 1: continue
                if move == 'D' and self.hwalls[r][c] == 1: continue
                if move == 'L' and self.vwalls[r][c-1] == 1: continue
                if move == 'R' and self.vwalls[r][c] == 1: continue
                
                if prev[nr][nc] is None:
                    prev[nr][nc] = (r, c, move)
                    q.append((nr, nc))

        if not found:
            self.cache[(start_node, goal_node)] = ([], [])
            return [], []

        path_nodes = []
        path_moves = []
        curr_r, curr_c = gr, gc
        while curr_r != sr or curr_c != sc:
            path_nodes.append((curr_r, curr_c))
            pr, pc, move = prev[curr_r][curr_c]
            path_moves.append(move)
            curr_r, curr_c = pr, pc
        path_nodes.append((sr, sc))
        path_nodes.reverse()
        path_moves.reverse()
        
        self.cache[(start_node, goal_node)] = (path_nodes, path_moves)
        return path_nodes, path_moves

# --- v8.0: StochasticBfsSolver (新規) ---
# ランダムな最短経路を生成する。キャッシュは使えない。
class StochasticBfsSolver:
    """
    壁情報を考慮したBFSを実行し、
    「ランダムな」最短経路を計算するクラス。(v8.0 新規)
    """
    def __init__(self, n, vwalls, hwalls):
        self.N = n
        self.vwalls = vwalls
        self.hwalls = hwalls
        self.moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
        # v8.0: キャッシュは使わない

    def solve(self, sr, sc, gr, gc):
        """
        (sr, sc) から (gr, gc) への「ランダムな」最短経路を計算します。
        """
        start_node = (sr, sc)
        goal_node = (gr, gc)
        
        q = deque([(sr, sc)])
        prev = [[None] * self.N for _ in range(self.N)]
        prev[sr][sc] = (-1, -1, 'S')
        
        # v8.0: 訪問済みを管理し、最短経路のステップ数を記録
        dist = [[-1] * self.N for _ in range(self.N)]
        dist[sr][sc] = 0
        
        found = False
        goal_dist = -1

        while q:
            r, c = q.popleft()
            
            if r == gr and c == gc:
                found = True
                goal_dist = dist[r][c]
                break
            
            # v8.0: 既にゴールが見つかっていて、それより遠い探索は打ち切る
            if goal_dist != -1 and dist[r][c] >= goal_dist:
                continue

            # v8.0: moves をシャッフルして探索順序をランダム化
            shuffled_moves = self.moves[:]
            random.shuffle(shuffled_moves)
            
            for dr, dc, move in shuffled_moves:
                nr, nc = r + dr, c + dc
                
                if not (0 <= nr < self.N and 0 <= nc < self.N): continue
                if move == 'U' and self.hwalls[r-1][c] == 1: continue
                if move == 'D' and self.hwalls[r][c] == 1: continue
                if move == 'L' and self.vwalls[r][c-1] == 1: continue
                if move == 'R' and self.vwalls[r][c] == 1: continue
                
                if prev[nr][nc] is None:
                    prev[nr][nc] = (r, c, move)
                    dist[nr][nc] = dist[r][c] + 1 # v8.0
                    q.append((nr, nc))

        if not found:
            return [], []

        # 経路復元
        path_nodes = []
        path_moves = []
        curr_r, curr_c = gr, gc
        while curr_r != sr or curr_c != sc:
            path_nodes.append((curr_r, curr_c))
            pr, pc, move = prev[curr_r][curr_c]
            path_moves.append(move)
            curr_r, curr_c = pr, pc
        path_nodes.append((sr, sc))
        path_nodes.reverse()
        path_moves.reverse()
        
        return path_nodes, path_moves

# --- v8.0: 評価関数 (v6.0 のロジック) ---
def calculate_solution(all_paths_info):
    """
    v8.0: 経路セット (all_paths_info) を受け取り、
    スコア (C+Q), C, Q, total_steps を計算して返す評価関数。
    (v6.0 の Step A～E をカプセル化)
    """
    
    # --- Step A: w (到着回数) の計算 ---
    w = [[0] * N for _ in range(N)]
    sr_k0, sc_k0 = TARGETS[0]
    w[sr_k0][sc_k0] += 1
    total_steps_X = 0
    
    for k in range(K - 1):
        path_nodes, path_moves = all_paths_info[k]
        if not path_nodes:
            # この経路セットは到達不能
            return 2 * (N**4) + K * (N**2), 1, 1, 0 
            
        total_steps_X += len(path_moves)
        for i in range(1, len(path_nodes)):
            r, c = path_nodes[i]
            w[r][c] += 1
            
    # v8.0: T 超過チェックのために total_steps_X を返す必要がある
    # if total_steps_X > T: # T はグローバル変数
    #     return 2 * (N**4) + K * (N**2), 1, 1, total_steps_X

    S_total_visits = sum(w[r][c] for r in range(N) for c in range(N))
    if S_total_visits == 0: # K=0?
        return 0, 1, 1, 0

    # --- Step B (v6): 全 S 回の訪問にユニーク ID を割り当て ---
    temp_visit_map = {}
    visit_id_to_item = [None] * S_total_visits
    start_visit_item = (sr_k0, sc_k0, 0)
    
    temp_visit_map[start_visit_item] = 0
    visit_id_to_item[0] = start_visit_item
    
    visit_id_counter = 1
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                if item == start_visit_item:
                    continue
                # v8.0: w[r][c]=0 のマスで k_item=0..-1 が発生するバグ対策
                if visit_id_counter >= S_total_visits:
                    break # S_total_visits を超えない
                temp_visit_map[item] = visit_id_counter
                visit_id_to_item[visit_id_counter] = item
                visit_id_counter += 1

    # --- Step C/D (v6): 全遷移 (A, S, D) タプルの計算 & ユニーク化 ---
    visit_count = [[0] * N for _ in range(N)]
    visit_to_transition = {}
    transition_to_rule_id = {}
    unique_transitions = []
    
    if K == 1:
        transition = (0, 0, 'S')
        visit_to_transition[start_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)
    
    for path_nodes, path_moves in all_paths_info:
        path_len = len(path_moves)
        for t in range(path_len):
            r, c = path_nodes[t]
            visit_k = visit_count[r][c]
            visit_count[r][c] += 1
            
            current_visit_item = (r, c, visit_k)
            if current_visit_item not in temp_visit_map:
                # v8.0: K>1 で T[k]=T[k+1] の場合、visit_count が w を超える
                # (例: T[1]=(5,5), T[2]=(5,5))
                # path_info[1] = ([], [])
                # visit_count[5,5] は増えるが w[5,5] は増えていない
                # この訪問は v6.0 では存在しなかった
                # (A_id, S_id) を計算できないため、この経路は無効
                return 2 * (N**4) + K * (N**2), 1, 1, total_steps_X


            if visit_k + 1 < w[r][c]:
                A_id = temp_visit_map[(r, c, visit_k + 1)]
            else:
                A_id = temp_visit_map[current_visit_item]
            
            nr, nc = path_nodes[t+1]
            visit_k_next = visit_count[nr][nc]
            
            # v8.0: (nr, nc) が w=0 (T[0]以外で未到着) のマスだった場合
            if (nr, nc, visit_k_next) not in temp_visit_map:
                 return 2 * (N**4) + K * (N**2), 1, 1, total_steps_X

            S_id = temp_visit_map[(nr, nc, visit_k_next)]
            D = path_moves[t]
            
            transition = (A_id, S_id, D)
            visit_to_transition[current_visit_item] = transition
            
            if transition not in transition_to_rule_id:
                transition_to_rule_id[transition] = len(unique_transitions)
                unique_transitions.append(transition)

    if K > 1:
        fr, fc = TARGETS[K-1]
        visit_k = visit_count[fr][fc]
        final_visit_item = (fr, fc, visit_k)
        
        if final_visit_item not in temp_visit_map:
             return 2 * (N**4) + K * (N**2), 1, 1, total_steps_X

        A_id = temp_visit_map[final_visit_item] 
        S_id = 0 
        D = 'S'
        
        transition = (A_id, S_id, D)
        visit_to_transition[final_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)

    # --- Step E (v6.0): 真の C, Q の計算 ---
    S_unique = len(unique_transitions)
    if S_unique == 0: # K=1 以外でありえない
        return 2 * (N**4) + K * (N**2), 1, 1, total_steps_X
        
    best_score = float('inf')
    Q_final = -1
    C_final = -1
    
    Q_ideal = max(1, int(math.sqrt(S_unique)))
    search_range_start = max(1, Q_ideal - 50)
    search_range_end = Q_ideal + 50
    if S_unique == 1:
        search_range_start = 1
        search_range_end = 1
    
    for Q_candidate in range(search_range_start, search_range_end + 1):
        C_candidate = (S_unique + Q_candidate - 1) // Q_candidate
        score = C_candidate + Q_candidate
        if score < best_score:
            best_score = score
            Q_final = Q_candidate
            C_final = C_candidate
            
    if Q_final == -1: Q_final, C_final = 1, 1

    return best_score, C_final, Q_final, total_steps_X

# --- v8.0: 出力関数 (v6.0 のロジック) ---
def generate_output_from_solution(all_paths_info, C_final, Q_final):
    """
    v8.0: 最適だった経路セットと (C, Q) を受け取り、
    最終的な解を stdout/stderr に出力する。
    (v6.0 の Step A～I をカプセル化)
    """
    
    # --- Step A: w (到着回数) の計算 ---
    w = [[0] * N for _ in range(N)]
    sr_k0, sc_k0 = TARGETS[0]
    w[sr_k0][sc_k0] += 1
    
    for k in range(K - 1):
        path_nodes, path_moves = all_paths_info[k]
        for i in range(1, len(path_nodes)):
            r, c = path_nodes[i]
            w[r][c] += 1
            
    S_total_visits = sum(w[r][c] for r in range(N) for c in range(N))
    if S_total_visits == 0:
        print_score(0); print(1, 1, 0); return

    # --- Step B (v6): 全 S 回の訪問にユニーク ID を割り当て ---
    temp_visit_map = {}
    visit_id_to_item = [None] * S_total_visits
    start_visit_item = (sr_k0, sc_k0, 0)
    
    temp_visit_map[start_visit_item] = 0
    visit_id_to_item[0] = start_visit_item
    
    visit_id_counter = 1
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                if item == start_visit_item:
                    continue
                if visit_id_counter >= S_total_visits: break
                temp_visit_map[item] = visit_id_counter
                visit_id_to_item[visit_id_counter] = item
                visit_id_counter += 1

    # --- Step C/D (v6): 全遷移 (A, S, D) タプルの計算 & ユニーク化 ---
    visit_count = [[0] * N for _ in range(N)]
    visit_to_transition = {}
    transition_to_rule_id = {}
    unique_transitions = []
    
    if K == 1:
        transition = (0, 0, 'S')
        visit_to_transition[start_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)
    
    for path_nodes, path_moves in all_paths_info:
        path_len = len(path_moves)
        for t in range(path_len):
            r, c = path_nodes[t]
            visit_k = visit_count[r][c]
            visit_count[r][c] += 1
            current_visit_item = (r, c, visit_k)

            # v8.0: calculate_solution でチェック済みなので、ここではエラーは起きないはず
            if current_visit_item not in temp_visit_map: continue 

            if visit_k + 1 < w[r][c]:
                A_id = temp_visit_map[(r, c, visit_k + 1)]
            else:
                A_id = temp_visit_map[current_visit_item]
            
            nr, nc = path_nodes[t+1]
            visit_k_next = visit_count[nr][nc]
            
            if (nr, nc, visit_k_next) not in temp_visit_map: continue

            S_id = temp_visit_map[(nr, nc, visit_k_next)]
            D = path_moves[t]
            
            transition = (A_id, S_id, D)
            visit_to_transition[current_visit_item] = transition
            
            if transition not in transition_to_rule_id:
                transition_to_rule_id[transition] = len(unique_transitions)
                unique_transitions.append(transition)

    if K > 1:
        fr, fc = TARGETS[K-1]
        visit_k = visit_count[fr][fc]
        final_visit_item = (fr, fc, visit_k)

        if final_visit_item not in temp_visit_map:
             print_score(2 * (N**4)); print(1, 1, 0); return # v8.0 安全策

        A_id = temp_visit_map[final_visit_item] 
        S_id = 0 
        D = 'S'
        
        transition = (A_id, S_id, D)
        visit_to_transition[final_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)

    S_unique = len(unique_transitions)
    if S_unique == 0:
        print_score(2 * (N**4)); print(1, 1, 0); return # v8.0 安全策

    # --- Step E (v6.0): C, Q は引数で受け取ったものを使う ---
    # (ここでは再計算しない)

    # --- Step F (v6): 新しい (c, q) ペアの割り当て ---
    rule_id_to_cq = {}
    
    start_transition = visit_to_transition[start_visit_item]
    start_rule_id = transition_to_rule_id[start_transition]
    
    rule_id_to_cq[start_rule_id] = (0, 0)
    
    slot_index = 1 
    for rule_id in range(S_unique):
        if rule_id == start_rule_id:
            continue
            
        q_val = slot_index % Q_final
        c_val = slot_index // Q_final
        
        if c_val >= C_final:
             q_val = 0
             c_val = 0
             
        rule_id_to_cq[rule_id] = (c_val, q_val)
        slot_index += 1

    # --- Step G (v6): new_visit_map (訪問 -> (c,q)) の構築 ---
    new_visit_map = {}
    s = [[-1] * N for _ in range(N)] # 初期盤面
    
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                
                if item not in visit_to_transition: continue # v8.0 安全策
                
                transition = visit_to_transition[item]
                rule_id = transition_to_rule_id[transition]
                
                c_val, q_val = rule_id_to_cq[rule_id]
                new_visit_map[item] = (c_val, q_val)
                
                if k_item == 0:
                    s[r_item][c_item] = c_val

    # --- Step H (v6): new_rules の構築 ---
    new_rules = {} 
    
    for rule_id in range(S_unique):
        c_in, q_in = rule_id_to_cq[rule_id]
        transition = unique_transitions[rule_id]
        A_id, S_id, D = transition
        
        if A_id >= S_total_visits or S_id >= S_total_visits: continue # v8.0 安全策
        
        A_item = visit_id_to_item[A_id]
        if A_item not in new_visit_map: continue
        A_color, _ = new_visit_map[A_item]
        
        S_item = visit_id_to_item[S_id]
        if S_item not in new_visit_map: continue
        _, S_state = new_visit_map[S_item]
        
        new_rules[(c_in, q_in)] = (A_color, S_state, D)

    # --- Step I (v6): 出力 ---
    for r in range(N):
        for c in range(N):
            if s[r][c] == -1:
                s[r][c] = 0
                
    M_final = len(new_rules)
    
    # 開発合意事項: スコアを stderr に出力
    final_score = C_final + Q_final
    print_score(final_score)
    
    # 1. C Q M
    print(f"{C_final} {Q_final} {M_final}")
    
    # 2. 初期盤面 s
    for r in range(N):
        print(" ".join(map(str, s[r])))
        
    # 3. 遷移規則 M
    for (c, q), (A, S, D) in new_rules.items():
        print(f"{c} {q} {A} {S} {D}")


def solve():
    """
    v8.0: 焼きなまし法 (SA) のメインループ
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    start_time = time.time()
    
    # 1. 決定論的BFS (キャッシュ有効) と 確率的BFS (キャッシュ無効) を用意
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    stoch_bfs_solver = StochasticBfsSolver(N, VWALLS, HWALLS)

    # 2. 初期解の生成 (v6.0 と同じ)
    initial_paths_info = []
    initial_total_steps = 0
    for k in range(K - 1):
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        
        # 決定論的BFS
        path_nodes, path_moves = bfs_solver.solve(sr, sc, gr, gc)
        
        if not path_nodes:
            # K>1 で到達不能 (v6.0 と同じ)
            print_score(2 * (N**4) + K * (N**2)); print(1, 1, 0)
            return
            
        initial_paths_info.append((path_nodes, path_moves))
        initial_total_steps += len(path_moves)

    # T 超過チェック (v6.0 には無かったが重要)
    if initial_total_steps > T:
        print_score(2 * (N**4) + K * (N**2)); print(1, 1, 0)
        return

    # 3. 初期解の評価
    best_score, best_C, best_Q, total_steps = calculate_solution(initial_paths_info)
    
    # v8.0: K=1 のエッジケース (SAループ不要)
    if K == 1:
        best_score, best_C, best_Q, total_steps = calculate_solution([])
        generate_output_from_solution([], best_C, best_Q)
        return

    current_score = best_score
    current_paths_info = initial_paths_info
    best_paths_info = initial_paths_info
    
    # v8.0: SA の温度設定
    # スコア (C+Q) は 20～100 程度。差分 delta は 1～10 程度を想定。
    T_start = 1.5 
    T_end = 0.01
    
    loop_count = 0
    
    # 4. 焼きなましループ
    while True:
        loop_count += 1
        current_time = time.time()
        time_ratio = (current_time - start_time) / 1.7
        
        if time_ratio >= 1.0:
            break # 1.7秒で打ち切り

        # a. 近傍操作: ランダムな 1 区間 (k) を選び、最短経路を再計算
        k = random.randint(0, K - 2)
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        
        # 確率的BFS
        new_path_nodes, new_path_moves = stoch_bfs_solver.solve(sr, sc, gr, gc)

        if not new_path_nodes:
            continue # 到達不能 (通常ありえない)
            
        # b. 新しい経路セット (new_paths_info) を構築
        new_paths_info = current_paths_info[:]
        new_paths_info[k] = (new_path_nodes, new_path_moves)
        
        # c. 新しい解の評価
        new_score, new_C, new_Q, new_total_steps = calculate_solution(new_paths_info)

        # d. T 超過チェック (v8.0 の最重要セーフティネット)
        if new_total_steps > T:
            continue # この近傍は T を超えるため破棄

        # e. 採択判定
        delta = new_score - current_score
        
        if delta < 0: # スコア改善
            current_score = new_score
            current_paths_info = new_paths_info
            
            if new_score < best_score:
                best_score = new_score
                best_paths_info = new_paths_info
                best_C = new_C
                best_Q = new_Q
                
        else: # スコア悪化
            # T_start から T_end へ線形に減少
            temp = T_start + (T_end - T_start) * time_ratio
            
            if temp > T_end and math.exp(-delta / temp) > random.random():
                # 悪化解を採択
                current_score = new_score
                current_paths_info = new_paths_info

    # 5. ループ終了後、最適解を出力
    # (v8.0: ループ回数をデバッグ出力)
    # print(f"Loop count: {loop_count}", file=sys.stderr) 
    generate_output_from_solution(best_paths_info, best_C, best_Q)


def read_input():
    """
    標準入力から問題文を読み込み、グローバル変数に設定します。
    (v6.0 と同一)
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    try:
        N, K, T = map(int, sys.stdin.readline().split())
        VWALLS = []
        for _ in range(N):
            VWALLS.append([int(c) for c in sys.stdin.readline().strip()])
        HWALLS = []
        for _ in range(N - 1):
            HWALLS.append([int(c) for c in sys.stdin.readline().strip()])
        TARGETS = []
        for _ in range(K):
            r, c = map(int, sys.stdin.readline().split())
            TARGETS.append((r, c))
    except Exception as e:
        print(f"入力の読み込み中にエラーが発生しました: {e}", file=sys.stderr)
        return False
    return True

def main():
    """
    メイン実行関数 (v6.0 と同一)
    """
    sys.setrecursionlimit(2000) 
    if not read_input():
        return
    solve()

if __name__ == "__main__":
    main()