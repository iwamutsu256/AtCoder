import sys
import math
from collections import deque
import time

# --- 開発規約: stderr へのスコア出力 ---
def print_score(score):
    """
    開発規約に基づき、最終的な絶対スコアを標準エラー出力に出力します。
    
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

class BfsSolver:
    """
    壁情報を考慮したBFS（幅優先探索）を実行し、最短経路を計算するクラス。
    (v5.5 と同一)
    """
    def __init__(self, n, vwalls, hwalls):
        self.N = n
        self.vwalls = vwalls
        self.hwalls = hwalls
        self.moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
        self.cache = {} # v5.5 には無かったが、v4 からキャッシュ機能を採用

    def solve(self, sr, sc, gr, gc):
        """
        (sr, sc) から (gr, gc) への最短経路を計算します。(キャッシュ利用)
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

def solve():
    """
    v6: ルール共通化 メインロジック
    1. Step A (v5.5): w[r][c] (到着回数) を計算
    2. Step B (v6): 全S回の訪問にユニークID (0..S-1) を割り当て
    3. Step C/D (v6): 全S回の訪問の (A, S, D) 遷移タプルを計算
    4. Step E (v6): S_unique (ユニークな遷移数) を元に、真の (C, Q) を計算
    5. Step F-H (v6): S_unique個のルールに (c,q) を割り当て、盤面とルールを再構築
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    start_time = time.time()
    
    # --- Step A: v5.1 経路計算 & w (到着回数) の計算 ---
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    w = [[0] * N for _ in range(N)]
    all_paths_info = []
    
    sr_k0, sc_k0 = TARGETS[0]
    w[sr_k0][sc_k0] += 1
    total_steps_X = 0
    
    for k in range(K - 1):
        if time.time() - start_time > 1.7: break 
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
            
    S_total_visits = sum(w[r][c] for r in range(N) for c in range(N))
    
    # --- Step B (v6): 全 S 回の訪問にユニーク ID を割り当て ---
    # visit_item = (r, c, k)
    # temp_visit_map: (r, c, k) -> visit_id
    # visit_id_to_item: visit_id -> (r, c, k)
    
    temp_visit_map = {}
    visit_id_to_item = [None] * S_total_visits
    
    start_visit_item = (sr_k0, sc_k0, 0)
    
    # visit_id = 0 はスタート地点(k=0)の訪問
    temp_visit_map[start_visit_item] = 0
    visit_id_to_item[0] = start_visit_item
    
    visit_id_counter = 1
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                if item == start_visit_item:
                    continue
                temp_visit_map[item] = visit_id_counter
                visit_id_to_item[visit_id_counter] = item
                visit_id_counter += 1

    # --- Step C/D (v6): 全遷移 (A, S, D) タプルの計算 & ユニーク化 ---
    
    visit_count = [[0] * N for _ in range(N)]
    
    # visit_to_transition: (r, c, k) -> transition_tuple
    visit_to_transition = {}
    
    # transition_to_rule_id: transition_tuple -> unique_rule_id
    transition_to_rule_id = {}
    
    # unique_transitions: unique_rule_id -> transition_tuple
    unique_transitions = []
    
    # K=1 (経路なし) のエッジケース
    if K == 1:
        # A_id = 0 (自分自身), S_id = 0 (状態0), D = 'S'
        transition = (0, 0, 'S')
        visit_to_transition[start_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)
    
    # K > 1 の場合
    for path_nodes, path_moves in all_paths_info:
        path_len = len(path_moves)
        for t in range(path_len):
            r, c = path_nodes[t]
            visit_k = visit_count[r][c]
            visit_count[r][c] += 1
            
            current_visit_item = (r, c, visit_k)
            # current_visit_id = temp_visit_map[current_visit_item] # (デバッグ用)

            # A (次色) の決定: (r, c) 自身の「次の訪問 k+1」の visit_id
            if visit_k + 1 < w[r][c]:
                A_id = temp_visit_map[(r, c, visit_k + 1)]
            else:
                A_id = temp_visit_map[current_visit_item] # 最後の訪問は自分自身を指す
            
            # S (次状態) の決定: 移動先 (nr, nc) の「次の訪問 k'」の visit_id
            nr, nc = path_nodes[t+1]
            visit_k_next = visit_count[nr][nc]
            S_id = temp_visit_map[(nr, nc, visit_k_next)]
            
            D = path_moves[t]
            
            transition = (A_id, S_id, D)
            visit_to_transition[current_visit_item] = transition
            
            # ユニークな遷移として登録
            if transition not in transition_to_rule_id:
                transition_to_rule_id[transition] = len(unique_transitions)
                unique_transitions.append(transition)

    # 最終目的地(K-1)の 'S' (Stay) ルール (K>1 の場合)
    if K > 1:
        fr, fc = TARGETS[K-1]
        visit_k = visit_count[fr][fc]
        final_visit_item = (fr, fc, visit_k)
        
        A_id = temp_visit_map[final_visit_item] # 自分自身
        S_id = 0 # 状態 0 (v6では visit_id=0 を S=0 の代わりに使う)
        D = 'S'
        
        transition = (A_id, S_id, D)
        visit_to_transition[final_visit_item] = transition
        if transition not in transition_to_rule_id:
            transition_to_rule_id[transition] = len(unique_transitions)
            unique_transitions.append(transition)

    # --- Step E (v6): 真の C, Q の計算 ---
    S_unique = len(unique_transitions)
    
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

    # --- Step F (v6): 新しい (c, q) ペアの割り当て ---
    
    # rule_id_to_cq: unique_rule_id -> (c_val, q_val)
    rule_id_to_cq = {}
    
    # 1. スタート地点の「遷移」に対応する rule_id を見つける
    start_transition = visit_to_transition[start_visit_item]
    start_rule_id = transition_to_rule_id[start_transition]
    
    # 2. スタート地点のルール(rule_id)に (c=0, q=0) を割り当て
    rule_id_to_cq[start_rule_id] = (0, 0)
    
    # 3. 残りの S_unique-1 個のルールに (c,q) を割り当て
    slot_index = 1
    for rule_id in range(S_unique):
        if rule_id == start_rule_id:
            continue
        q_val = slot_index % Q_final
        c_val = slot_index // Q_final
        rule_id_to_cq[rule_id] = (c_val, q_val)
        slot_index += 1

    # --- Step G (v6): new_visit_map (訪問 -> (c,q)) の構築 ---
    
    # new_visit_map: (r, c, k) -> (c_val, q_val)
    new_visit_map = {}
    s = [[-1] * N for _ in range(N)] # 初期盤面
    
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                
                # 1. この訪問がどの遷移(ルール)を使うか特定
                transition = visit_to_transition[item]
                rule_id = transition_to_rule_id[transition]
                
                # 2. そのルールに割り当てられた (c,q) を取得
                c_val, q_val = rule_id_to_cq[rule_id]
                new_visit_map[item] = (c_val, q_val)
                
                # 3. k=0 回目の訪問 (初回) なら、初期色 s[r][c] を確定
                if k_item == 0:
                    s[r_item][c_item] = c_val

    # --- Step H (v6): new_rules の構築 ---
    
    new_rules = {} # (c_in, q_in) -> (A_color, S_state, D)
    
    for rule_id in range(S_unique):
        # 1. このルールの入力 (c_in, q_in)
        c_in, q_in = rule_id_to_cq[rule_id]
        
        # 2. このルールの遷移タプル (A_id, S_id, D)
        transition = unique_transitions[rule_id]
        A_id, S_id, D = transition
        
        # 3. A_id (次の色) と S_id (次の状態) を (c,q) にデコード
        
        # A_id (visit_id) が指す訪問 (r,c,k)
        A_item = visit_id_to_item[A_id]
        # その訪問が使う (c,q) ペア
        A_color, _ = new_visit_map[A_item]
        
        # S_id (visit_id) が指す訪問 (r,c,k)
        S_item = visit_id_to_item[S_id]
        # その訪問が使う (c,q) ペア
        _, S_state = new_visit_map[S_item]
        
        new_rules[(c_in, q_in)] = (A_color, S_state, D)

    # --- Step I (v6): 出力 ---
    
    # s[r][c] == -1 のマス (一度も訪問しないマス) に色0を割り当てる
    for r in range(N):
        for c in range(N):
            if s[r][c] == -1:
                s[r][c] = 0
                
    M_final = len(new_rules) # S_unique と一致するはず
    
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


def read_input():
    """
    標準入力から問題文を読み込み、グローバル変数に設定します。
    (v5.5 と同一)
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
    メイン実行関数 (v5.5 と同一)
    """
    sys.setrecursionlimit(2000) 
    if not read_input():
        return
    solve()

if __name__ == "__main__":
    main()