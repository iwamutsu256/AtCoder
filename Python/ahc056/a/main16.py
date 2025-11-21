import sys
import math
from collections import deque
import time
import random
import copy

# --- 開発規約: stderr へのスコア出力 ---
def print_score(score):
    """
    開発規約に基づき、最終的な絶対スコアを標準エラー出力に出力します。
    """
    print(score, file=sys.stderr)

# --- グローバル変数 (入力から設定) ---
N = 0
K = 0
T = 0
VWALLS = []
HWALLS = []
TARGETS = []

# --- BfsSolver (v12 と同一) ---
class BfsSolver:
    """
    壁情報を考慮したBFS（幅優先探索）を実行し、最短経路を計算するクラス。
    """
    def __init__(self, n, vwalls, hwalls):
        self.N = n
        self.vwalls = vwalls
        self.hwalls = hwalls
        self.moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
        self.cache = {}

    def is_valid(self, r, c):
        return 0 <= r < self.N and 0 <= c < self.N

    def solve(self, sr, sc, gr, gc):
        """
        (sr, sc) から (gr, gc) への最短経路を計算します。(キャッシュ利用)
        """
        start_node = (sr, sc)
        goal_node = (gr, gc)
        
        if (start_node, goal_node) in self.cache:
            return copy.deepcopy(self.cache[(start_node, goal_node)])

        q = deque([(sr, sc)])
        prev = [[None] * self.N for _ in range(self.N)]
        prev[sr][sc] = (-1, -1, 'S')
        
        found = False
        while q:
            r, c = q.popleft()
            if r == gr and c == gc:
                found = True
                break
            
            for dr, dc, move in self.moves:
                nr, nc = r + dr, c + dc
                
                if not self.is_valid(nr, nc): continue
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
        return copy.deepcopy((path_nodes, path_moves))

# --- v14: 評価関数 (v6ロジックの Step B' ~ E) ---
def calc_v14_evaluation(state_visit_order, all_paths_info, w, sr_k0, sc_k0):
    """
    v14: 焼きなまし法の評価関数
    与えられた「訪問順序 (state_visit_order)」に基づき、
    v6 の Step B' (ID割り当て), C/D (遷移計算), E (C+Q計算) を実行し、
    最終的な C+Q スコアを返す。
    
    Args:
        state_visit_order (list): (r, c, k) のタプルのリスト (シャッフルされた状態)
        all_paths_info (list): v6 Step A で計算した固定の経路
        w (list[list]): v6 Step A で計算した固定の訪問回数マップ
        sr_k0, sc_k0 (int, int): スタート地点
    
    Returns:
        int: C+Q スコア (失敗時は float('inf'))
    """
    
    S_total_visits = len(state_visit_order)
    
    # --- Step B' (v14): state_visit_order に基づき ID を割り当て ---
    temp_visit_map = {}
    visit_id_to_item = [None] * S_total_visits
    start_visit_item = (sr_k0, sc_k0, 0)
    
    start_visit_id = -1
    
    # 1. state_visit_order に基づき、visit_id (0..S-1) を割り当てる
    for visit_id, item in enumerate(state_visit_order):
        temp_visit_map[item] = visit_id
        visit_id_to_item[visit_id] = item
        if item == start_visit_item:
            start_visit_id = visit_id
            
    if start_visit_id == -1:
        # (ありえないはずだが)
        return float('inf')

    # --- Step C/D (v6): 全遷移 (A, S, D) タプルの計算 & ユニーク化 ---
    # (v6とロジックは同一だが、ID割り当てが v14 順序に依存)
    visit_count = [[0] * N for _ in range(N)]
    visit_to_transition = {}
    transition_to_rule_id = {}
    unique_transitions = []
    
    if K == 1:
        # K=1 の場合、start_visit_id = 0
        transition = (start_visit_id, start_visit_id, 'S')
        visit_to_transition[start_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = 0
            unique_transitions.append(transition)
    
    if K > 1:
        for path_nodes, path_moves in all_paths_info:
            path_len = len(path_moves)
            for t in range(path_len):
                r, c = path_nodes[t]
                visit_k = visit_count[r][c]
                visit_count[r][c] += 1
                
                current_visit_item = (r, c, visit_k)

                if visit_k + 1 < w[r][c]:
                    A_id = temp_visit_map[(r, c, visit_k + 1)]
                else:
                    A_id = temp_visit_map[current_visit_item]
                
                nr, nc = path_nodes[t+1]
                visit_k_next = visit_count[nr][nc]
                S_id = temp_visit_map[(nr, nc, visit_k_next)]
                
                D = path_moves[t]
                transition = (A_id, S_id, D)
                visit_to_transition[current_visit_item] = transition
                
                if transition not in transition_to_rule_id:
                    transition_to_rule_id[transition] = len(unique_transitions)
                    unique_transitions.append(transition)

        fr, fc = TARGETS[K-1]
        visit_k = visit_count[fr][fc]
        final_visit_item = (fr, fc, visit_k)
        A_id = temp_visit_map[final_visit_item]
        S_id = start_visit_id # S=0 の代わりに、スタート地点のIDを使う
        D = 'S'
        transition = (A_id, S_id, D)
        visit_to_transition[final_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)

    # --- Step E (v6): 真の C, Q の計算 ---
    S_unique = len(unique_transitions)
    if S_unique == 0:
        return 2
        
    best_score = float('inf')
    Q_final = -1
    C_final = -1
    
    Q_ideal = max(1, int(math.sqrt(S_unique)))
    # (v14: 評価関数なので、探索範囲は狭くても良い)
    search_range_start = max(1, Q_ideal - 10)
    search_range_end = min(Q_ideal + 10, S_unique)
    
    for Q_candidate in range(search_range_start, search_range_end + 1):
        C_candidate = (S_unique + Q_candidate - 1) // Q_candidate
        score = C_candidate + Q_candidate
        if score < best_score:
            best_score = score
            Q_final = Q_candidate
            C_final = C_candidate
            
    if Q_final == -1: 
        Q_final, C_final = 1, S_unique

    final_score = C_final + Q_final
    
    # 評価関数は C+Q スコアのみを返す
    return final_score


def solve():
    """
    v14: 「訪問IDの割り当て順序」焼きなまし法
    v6 の Step A (経路・w計算) は固定。
    v6 の Step B (visit_id 割り当て) の「順序」をSAの状態とし、
    v6 の Step C-E (S_unique と C+Q の計算) を評価関数として、
    C+Q が最小になる「訪問順序」を探す。
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    
    start_time = time.time()
    time_limit = start_time + 1.8 # 実行時間制限 (秒)
    
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    
    # --- Step A: v6 (貪欲) の初期解を計算 (固定) ---
    all_paths_info = []
    w = [[0] * N for _ in range(N)]
    sr_k0, sc_k0 = TARGETS[0]
    w[sr_k0][sc_k0] += 1
    total_steps_X = 0
    
    for k in range(K - 1):
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        path_nodes, path_moves = bfs_solver.solve(sr, sc, gr, gc)
        
        if not path_nodes:
            print_score(2 * (N**4) + K * (N**2)); print(1, 1, 0)
            return
            
        all_paths_info.append((path_nodes, path_moves))
        total_steps_X += len(path_moves)
        for i in range(1, len(path_nodes)):
            r, c = path_nodes[i]
            w[r][c] += 1
    
    if total_steps_X > T:
        print_score(2 * (N**4) + K * (N**2)); print(1, 1, 0)
        return

    # --- v14: SA の初期状態 (v6 と同じ機械的な訪問順序) を作成 ---
    S_total_visits = sum(w[r][c] for r in range(N) for c in range(N))
    current_state_visit_order = [None] * S_total_visits
    
    start_visit_item = (sr_k0, sc_k0, 0)
    current_state_visit_order[0] = start_visit_item # v6 は 0 をスタートに割り当て
    
    visit_id_counter = 1
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                if item == start_visit_item:
                    continue
                current_state_visit_order[visit_id_counter] = item
                visit_id_counter += 1

    # --- 初期解 (v6) の評価 ---
    current_score = calc_v14_evaluation(current_state_visit_order, all_paths_info, w, sr_k0, sc_k0)
    best_score = current_score
    best_state_visit_order = copy.deepcopy(current_state_visit_order)
    
    # --- 焼きなまし法パラメータ ---
    start_temp = 5.0
    end_temp = 0.1
    
    iter_count = 0
    
    # --- v14: 焼きなましループ ---
    while True:
        iter_count += 1
        current_time = time.time()
        if current_time >= time_limit:
            break
            
        # --- 1. 近傍操作 (v14: 訪問順序の swap) ---
        
        if S_total_visits <= 1:
            break
            
        # (a) スタート地点 (ID=0) は動かさない方が良いかもしれない
        # (v6 は 0 を特別扱いしていたが、v14評価関数は start_visit_id を使う)
        # (いや、v6 の Step F は start_rule_id を (0,0) に固定していた...)
        
        # (a) ランダムな2つのインデックス i, j を選択
        i = random.randint(0, S_total_visits - 1)
        j = random.randint(0, S_total_visits - 1)
        if i == j:
            continue
            
        # (b) swap
        current_state_visit_order[i], current_state_visit_order[j] = \
            current_state_visit_order[j], current_state_visit_order[i]
        
        # --- 2. 新しい状態 (訪問順序) の評価 ---
        new_score = calc_v14_evaluation(current_state_visit_order, all_paths_info, w, sr_k0, sc_k0)

        # --- 3. 焼きなまし受容判定 ---
        temp_progress = (current_time - start_time) / (time_limit - start_time)
        temp_now = start_temp * ((1.0 - temp_progress) ** 2) + end_temp
        
        delta = new_score - current_score
        
        if delta <= 0 or (temp_now > 0 and random.random() < math.exp(-delta / temp_now)):
            # 受容: 状態を更新
            current_score = new_score
            
            if new_score < best_score:
                best_score = new_score
                best_state_visit_order = copy.deepcopy(current_state_visit_order)
        else:
            # 棄却: 状態を元に戻す (swap し直す)
            current_state_visit_order[i], current_state_visit_order[j] = \
                current_state_visit_order[j], current_state_visit_order[i]

    # --- SA ループ終了 ---
    
    # print(f"Iter: {iter_count}", file=sys.stderr) # デバッグ用
    
    # --- 最終出力: ベストな訪問順序 (best_state) を使って、v6 の Step B-H を実行 ---
    
    # (v14評価関数は C+Q しか返さなかったので、v6ロジックを再実行)
    
    # --- Step B' (v14) ---
    temp_visit_map = {}
    visit_id_to_item = [None] * S_total_visits
    start_visit_id = -1
    
    for visit_id, item in enumerate(best_state_visit_order):
        temp_visit_map[item] = visit_id
        visit_id_to_item[visit_id] = item
        if item == start_visit_item:
            start_visit_id = visit_id

    # --- Step C/D (v6) ---
    visit_count = [[0] * N for _ in range(N)]
    visit_to_transition = {}
    transition_to_rule_id = {}
    unique_transitions = []
    
    if K == 1:
        transition = (start_visit_id, start_visit_id, 'S')
        visit_to_transition[start_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = 0
            unique_transitions.append(transition)
    
    if K > 1:
        for path_nodes, path_moves in all_paths_info:
            path_len = len(path_moves)
            for t in range(path_len):
                r, c = path_nodes[t]
                visit_k = visit_count[r][c]
                visit_count[r][c] += 1
                current_visit_item = (r, c, visit_k)

                if visit_k + 1 < w[r][c]:
                    A_id = temp_visit_map[(r, c, visit_k + 1)]
                else:
                    A_id = temp_visit_map[current_visit_item]
                nr, nc = path_nodes[t+1]
                visit_k_next = visit_count[nr][nc]
                S_id = temp_visit_map[(nr, nc, visit_k_next)]
                D = path_moves[t]
                transition = (A_id, S_id, D)
                visit_to_transition[current_visit_item] = transition
                
                if transition not in transition_to_rule_id:
                    transition_to_rule_id[transition] = len(unique_transitions)
                    unique_transitions.append(transition)

        fr, fc = TARGETS[K-1]
        visit_k = visit_count[fr][fc]
        final_visit_item = (fr, fc, visit_k)
        A_id = temp_visit_map[final_visit_item]
        S_id = start_visit_id
        D = 'S'
        transition = (A_id, S_id, D)
        visit_to_transition[final_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)

    # --- Step E (v6) ---
    S_unique = len(unique_transitions)
    if S_unique == 0: S_unique = 1 # (K=1で S_unique=1 になるはず)
        
    best_score_E = float('inf')
    Q_final = -1
    C_final = -1
    
    Q_ideal = max(1, int(math.sqrt(S_unique)))
    search_range_start = max(1, Q_ideal - 50) # 最後は広めに探索
    search_range_end = min(Q_ideal + 50, S_unique)
    
    for Q_candidate in range(search_range_start, search_range_end + 1):
        C_candidate = (S_unique + Q_candidate - 1) // Q_candidate
        score = C_candidate + Q_candidate
        if score < best_score_E:
            best_score_E = score
            Q_final = Q_candidate
            C_final = C_candidate
            
    if Q_final == -1: Q_final, C_final = 1, S_unique
    
    final_score = C_final + Q_final
    
    # (SA が見つけた best_score と、最後の Step E の計算がずれる可能性
    #  (Q探索範囲) があるが、最終出力は Step E の C, Q に従う)

    # --- Step F (v6) ---
    rule_id_to_cq = {}
    
    # (v14: スタート地点の「ルール」が (0,0) を取る)
    start_transition = visit_to_transition[start_visit_item]
    start_rule_id = transition_to_rule_id[start_transition]
    rule_id_to_cq[start_rule_id] = (0, 0)
    
    slot_index = 1
    for rule_id in range(S_unique):
        if rule_id == start_rule_id:
            continue
        q_val = slot_index % Q_final
        c_val = slot_index // Q_final
        rule_id_to_cq[rule_id] = (c_val, q_val)
        slot_index += 1

    # --- Step G (v6) ---
    new_visit_map = {}
    s_board = [[-1] * N for _ in range(N)]
    
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                
                transition = visit_to_transition[item]
                rule_id = transition_to_rule_id[transition]
                
                c_val, q_val = rule_id_to_cq[rule_id]
                new_visit_map[item] = (c_val, q_val)
                
                if k_item == 0:
                    s_board[r_item][c_item] = c_val

    # --- Step H (v6) ---
    final_rules = {}
    
    for rule_id in range(S_unique):
        c_in, q_in = rule_id_to_cq[rule_id]
        transition = unique_transitions[rule_id]
        A_id, S_id, D = transition
        
        A_item = visit_id_to_item[A_id]
        A_color, _ = new_visit_map[A_item]
        
        S_item = visit_id_to_item[S_id]
        _, S_state = new_visit_map[S_item]
        
        final_rules[(c_in, q_in)] = (A_color, S_state, D)

    # --- Step I (v6) ---
    for r in range(N):
        for c in range(N):
            if s_board[r][c] == -1:
                s_board[r][c] = 0
                
    M_final = len(final_rules)
    
    print_score(final_score)
    
    print(f"{C_final} {Q_final} {M_final}")
    
    for r in range(N):
        print(" ".join(map(str, s_board[r])))
        
    for (c, q), (A, S, D) in final_rules.items():
        print(f"{c} {q} {A} {S} {D}")


def read_input():
    """
    標準入力から問題文を読み込み、グローバル変数に設定します。
    (v6 と同一)
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
    メイン実行関数 (v6 と同一)
    """
    sys.setrecursionlimit(4000)
    if not read_input():
        return
    solve()

if __name__ == "__main__":
    main()