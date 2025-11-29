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

# --- 経路探索クラス ---
class BfsSolver:
    """
    壁情報を考慮したBFS（幅優先探索）を実行し、最短経路を計算するクラス。
    """
    def __init__(self, n, vwalls, hwalls):
        """
        コンストラクタ。
        Args:
            n (int): グリッドサイズ (N x N)
            vwalls (list[list[int]]): 垂直方向の壁情報
            hwalls (list[list[int]]): 水平方向の壁情報
        """
        self.N = n
        self.vwalls = vwalls
        self.hwalls = hwalls
        self.moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]

    def solve(self, sr, sc, gr, gc):
        """
        (sr, sc) から (gr, gc) への最短経路を計算します。
        
        Args:
            sr (int): スタート行
            sc (int): スタート列
            gr (int): ゴール行
            gc (int): ゴール列
            
        Returns:
            tuple: (path_nodes, path_moves)
                path_nodes (list[tuple]): (r, c) のリスト (スタートからゴールまで)
                path_moves (list[str]): 'U', 'D', 'L', 'R' の移動方向リスト
        """
        q = deque([(sr, sc)])
        # prev[r][c] = (pr, pc, move)
        prev = [[None] * self.N for _ in range(self.N)]
        prev[sr][sc] = (-1, -1, 'S') # スタート地点のマーカー
        
        found = False
        while q:
            r, c = q.popleft()
            if r == gr and c == gc:
                found = True
                break
            
            for dr, dc, move in self.moves:
                nr, nc = r + dr, c + dc
                
                if not (0 <= nr < self.N and 0 <= nc < self.N):
                    continue
                
                # 壁チェック
                if move == 'U' and self.hwalls[r-1][c] == 1: continue
                if move == 'D' and self.hwalls[r][c] == 1: continue
                if move == 'L' and self.vwalls[r][c-1] == 1: continue
                if move == 'R' and self.vwalls[r][c] == 1: continue
                
                if prev[nr][nc] is None:
                    prev[nr][nc] = (r, c, move)
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

def create_full_path_sequence(bfs_solver):
    """
    Step A: 全ターゲット間の最短経路を計算し、全行程を一本の訪問シーケンスとして生成する。
    
    Returns:
        tuple: (full_path_nodes, full_path_moves, total_steps)
            full_path_nodes (list[tuple]): 全行程の (r, c) 座標シーケンス
            full_path_moves (list[str]): 全行程の移動方向シーケンス
            total_steps (int): 全ステップ数
    """
    # all_paths_info: 各区間ごとの経路情報
    all_paths_info = []
    total_steps = 0
    
    for k in range(K - 1):
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        path_nodes, path_moves = bfs_solver.solve(sr, sc, gr, gc)
        if not path_nodes:
            return None, None, -1 # 到達不能
        all_paths_info.append((path_nodes, path_moves))
        total_steps += len(path_moves)

    # 全行程を一本のシーケンスにまとめる
    full_path_nodes = []
    full_path_moves = []
    sr, sc = TARGETS[0]
    full_path_nodes.append((sr, sc))

    for path_nodes, path_moves in all_paths_info:
        # 各区間の経路を追加 (スタート地点は重複させない)
        full_path_nodes.extend(path_nodes[1:])
        full_path_moves.extend(path_moves)

    return full_path_nodes, full_path_moves, total_steps

def find_optimal_cq(total_visits):
    """
    Step B: 総訪問回数 total_visits に対し、C*Q >= total_visits を満たし
    C+Q を最小化する最適な (C, Q) を探索する。
    """
    if total_visits == 0:
        return 1, 1

    best_score = float('inf')
    Q_final, C_final = -1, -1
    
    # 理論上の最適値 Q_ideal は sqrt(total_visits) 付近
    Q_ideal = max(1, int(math.sqrt(total_visits)))
    
    # 探索範囲を Q_ideal の周辺に設定
    search_range_start = max(1, Q_ideal - 50)
    search_range_end = min(Q_ideal + 50, total_visits) # Qはtotal_visitsを超える必要はない
    
    for Q_candidate in range(search_range_start, search_range_end + 1):
        # C_candidate = ceil(total_visits / Q)
        C_candidate = (total_visits + Q_candidate - 1) // Q_candidate
        score = C_candidate + Q_candidate
        
        if score < best_score:
            best_score = score
            Q_final = Q_candidate
            C_final = C_candidate
            
    if Q_final == -1:
        # 探索範囲で見つからなかった場合 (total_visitsが小さい場合など)
        return 1, total_visits

    return C_final, Q_final

def generate_rules_and_board_dynamically(full_path_nodes, full_path_moves):
    """
    Step B,C,D: 全行程シーケンスを逆順に辿り、ルールと初期盤面を動的に生成する。
    「(A, S, D) -> (c, q)」のマッピングを動的に構築し、ルールを共通化する。
    新しい(c,q)が必要になるたび、CとQを動的に拡張する。
    """
    total_visits = len(full_path_nodes)
    if total_visits == 0:
        return {}, [[0]*N for _ in range(N)], 1, 1

    # --- 初期化 ---
    C_current, Q_current = 1, 1
    used_cq_slots = set()
    transition_to_cq = {}
    step_to_cq = {}
    pos_to_future_color = {}
    initial_board = [[0] * N for _ in range(N)] # 要望: 最初は全て0

    def assign_new_cq():
        """利用可能な新しい(c,q)を探し、なければCかQを拡張する"""
        nonlocal C_current, Q_current
        # Cを優先して探索 (ジグザグ探索)
        for q in range(Q_current):
            for c in range(C_current):
                if (c, q) not in used_cq_slots:
                    used_cq_slots.add((c, q))
                    return c, q
        
        # 空きがないのでCかQを拡張
        # Cを増やすかQを増やすか、C+Qが小さくなる方を選ぶ
        # CがQ+2以上になることを防ぐ
        if C_current > Q_current:
            Q_current += 1
            c_start, q_start = 0, Q_current - 1
            c, q = 0, Q_current - 1
        else:
            C_current += 1
            c_start, q_start = C_current - 1, 0
        
        c, q = c_start, q_start
        # 拡張したスロットが既に使用済みの場合(非常に稀だが)、空きを探す
        while (c, q) in used_cq_slots:
            if C_current > Q_current:
                c = (c + 1) % C_current
            else:
                q = (q + 1) % Q_current
                if q == q_start: # 1周したらcをインクリメント
                    c = (c + 1) % C_current
            c, q = C_current - 1, 0

        used_cq_slots.add((c, q))
        return c, q

    # --- 逆順ループ ---
    for t in reversed(range(total_visits)):
        pos = full_path_nodes[t]

        # 1. 遷移(A, S, D)を決定
        if t + 1 < total_visits:
            _, S = step_to_cq[t + 1]
            D = full_path_moves[t]
        else: # 最終ステップ
            S, D = 0, 'S'

        if pos in pos_to_future_color:
            A = pos_to_future_color[pos]
        else: # このマスへのこれ以降の訪問はない
            A = 0 # 最後の訪問なので、色0を書き込む
            # 最後の訪問なので、次に書き込む色は0 (ゴール後盤面を0にする)
            # ただし、このステップで読み取るべき色c_inが決まっていないので、
            # プレースホルダとして-1を使い、後でc_inで置き換える
            A = -1

        transition = (A, S, D)

        # 2. 遷移に対応する(c,q)を取得 or 新規割り当て
        if transition not in transition_to_cq:
            c_in, q_in = assign_new_cq()
            transition_to_cq[transition] = (c_in, q_in)
        else:
            c_in, q_in = transition_to_cq[transition]
        
        # プレースホルダA=-1だった場合、今決まったc_inで遷移キーを更新
        if A == -1:
            new_transition = (c_in, S, D)
            if new_transition != transition:
                del transition_to_cq[transition]
                transition_to_cq[new_transition] = (c_in, q_in)

        step_to_cq[t] = (c_in, q_in)

        # 3. このマスに将来訪れる場合、この色c_inを読む必要がある
        pos_to_future_color[pos] = c_in

    # --- 最終的なルールと初期盤面を生成 ---
    rules = {cq: trans for trans, cq in transition_to_cq.items()}
    
    # pos_to_future_color には、各マスに初回訪問する際に
    # 読み取るべき色が記録されている。
    for pos, color in pos_to_future_color.items():
        r, c = pos
        initial_board[r][c] = color

    return rules, initial_board, C_current, Q_current

def solve():
    """
    メインロジック
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    
    # Step A: 全行程のシーケンスを作成
    full_path_nodes, full_path_moves, total_steps = create_full_path_sequence(bfs_solver)

    if full_path_nodes is None or total_steps > T:
        print_score(2 * (N**4) + K * (N**2))
        print(1, 1, 0)
        return

    # Step B, C, D: 逆順にルールを決定し、共通化し、盤面を生成
    rules, initial_board, C_final, Q_final = generate_rules_and_board_dynamically(
        full_path_nodes, 
        full_path_moves
    )
    
    # --- Step F: 出力 ---
    M_final = len(rules)
    final_score = C_final + Q_final
    print_score(final_score)
    
    print(f"{C_final} {Q_final} {M_final}")
    for r in range(N):
        print(" ".join(map(str, initial_board[r])))
    for (c, q), (A, S, D) in rules.items():
        print(f"{c} {q} {A} {S} {D}")


def read_input():
    """
    標準入力から問題文を読み込み、グローバル変数に設定します。
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
    メイン実行関数
    """
    sys.setrecursionlimit(2000) 
    if not read_input():
        return
    solve()

if __name__ == "__main__":
    main()