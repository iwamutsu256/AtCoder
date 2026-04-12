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

def solve():
    """
    v5.5 メインロジック
    1. v5.1: w[r][c] (到着回数) を正確に計算
    2. v5.4: S = sum(w) に基づき、C*Q >= S となる C+Q が最小の (C, Q) を探索
    3. v5.3: (c,q)ペア割り当て。スタート(sr,sc,0)を(0,0)に固定
    4. v5.5: 状態連鎖を正しく繋ぐルール生成 (A=次訪問色, S=移動先状態)
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    
    # 実行開始時間
    start_time = time.time()
    
    # --- Step A: v5.1 経路計算 & w (到着回数) の計算 ---
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    
    # w[r][c] = マス(r,c) に「到着する」回数
    w = [[0] * N for _ in range(N)]
    all_paths_info = []
    
    # 1. スタート地点 k=0 への「到着」
    sr, sc = TARGETS[0]
    w[sr][sc] += 1
    
    total_steps_X = 0 # 全移動回数 (Tと比較用)
    
    for k in range(K - 1):
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        
        # 制限時間チェック (BFS前)
        if time.time() - start_time > 1.7:
             # 時間切れの場合は空の経路情報でwを確定させる
             # (v4までのロジック。実際にはT/Oする前にBFSが終わるはず)
             break 
             
        path_nodes, path_moves = bfs_solver.solve(sr, sc, gr, gc)
        
        if not path_nodes:
            # 経路が見つからない (入力の仮定に反する)
            print_score(2 * (N**4) + K * (N**2)) # Fail
            print(1, 1, 0)
            return
            
        all_paths_info.append((path_nodes, path_moves))
        total_steps_X += len(path_moves)
        
        # 2. k=1 から k=K-1 への「到着」
        # path_nodes[0] は (sr, sc)
        # path_nodes[1:] が移動先のノード (到着するマス)
        for i in range(1, len(path_nodes)):
            r, c = path_nodes[i]
            w[r][c] += 1
            
    # S (総訪問回数) = 全到着回数の合計
    # スタート地点(k=0)の1回 + 全経路の総ステップ数(X)
    S_total_visits = sum(w[r][c] for r in range(N) for c in range(N))
    
    # S_total_visits == total_steps_X + 1 のはず
    
    # --- Step B: v5.4 最適な Q と C の探索 ---
    # C * Q >= S_total_visits を満たし C+Q を最小化する
    
    best_score = float('inf')
    Q_final = -1
    C_final = -1
    
    # Q の探索範囲 (v5: Q_min は 1)
    # 理論上の最適値 Q_ideal は sqrt(S) 付近
    Q_ideal = max(1, int(math.sqrt(S_total_visits)))
    
    # 探索範囲を Q_ideal の周辺に設定
    search_range_start = max(1, Q_ideal - 50)
    search_range_end = Q_ideal + 50
    
    # K=1 (S=1) のエッジケース
    if S_total_visits == 1:
        search_range_start = 1
        search_range_end = 1
    
    for Q_candidate in range(search_range_start, search_range_end + 1):
        
        # C_candidate: Q_candidate のときに必要な最小の色数
        # math.ceil(S / Q) と同等
        C_candidate = (S_total_visits + Q_candidate - 1) // Q_candidate
        
        score = C_candidate + Q_candidate
        
        if score < best_score:
            best_score = score
            Q_final = Q_candidate
            C_final = C_candidate
            
    if Q_final == -1:
        # K=0 など、万が一探索されなかった場合 (S=0)
        Q_final, C_final = 1, 1

    # --- Step C: v5.3 (c, q) ペアの割り当て ---
    
    visit_map = {} # (r, c, k) -> (c_val, q_val)
    items_to_assign = [] # (r, c, k) のリスト (S-1個)
    
    # スタート地点の「最初の訪問」タプルを定義
    start_r, start_c = TARGETS[0]
    start_visit_item = (start_r, start_c, 0) # (sr, sc, 0回目)

    # 訪問する (行, 列, k回目) のタプルリストを作成
    for r_item in range(N):
        for c_item in range(N):
            for k_item in range(w[r_item][c_item]):
                item = (r_item, c_item, k_item)
                # スタート地点の最初の訪問(item)は、リストから除外
                if item == start_visit_item:
                    continue
                items_to_assign.append(item)

    # 1. 核心: スタート地点(k=0)の0回目の訪問に (c=0, q=0) を強制割り当て
    visit_map[start_visit_item] = (0, 0)
    
    # 2. 残りの S-1 個の訪問に (c,q) を割り当て
    #    (0,0) を避けるため、i+1 のインデックス(スロット)を使う
    for i in range(len(items_to_assign)):
        r_item, c_item, k_item = items_to_assign[i]
        
        # 訪問ID i (0 .. S-2) を C*Q グリッドのスロット (1 .. S-1) にマッピング
        slot_index = i + 1 # (0,0) スロットは使用済み
        
        q_val = slot_index % Q_final 
        c_val = slot_index // Q_final
        
        visit_map[(r_item, c_item, k_item)] = (c_val, q_val)

    # --- Step D: v5.5 遷移規則 M の生成 (核心部) ---
    visit_count = [[0] * N for _ in range(N)]
    rules = {}
    # s[r][c] = マス(r,c) の「初期色」
    s = [[-1] * N for _ in range(N)]
    
    # 核心: スタート地点(k=0) の初期色 s[sr][sc] を確定
    sr, sc = TARGETS[0]
    visit_k_start = visit_count[sr][sc] # 0
    c_in_start, q_in_start = visit_map[(sr, sc, visit_k_start)] # (0, 0)
    s[sr][sc] = c_in_start # s[sr][sc] = 0
    
    # K=1 (経路が 0本) のエッジケース
    if K == 1:
        # s[sr][sc] は 0 で確定済み
        rules[(c_in_start, q_in_start)] = (c_in_start, 0, 'S')
    
    # K > 1 の場合
    for path_nodes, path_moves in all_paths_info:
        path_len = len(path_moves)
        
        for t in range(path_len):
            # --- 現在の (c, q) を決定 ---
            r, c = path_nodes[t]
            visit_k = visit_count[r][c] # k回目
            visit_count[r][c] += 1      # 次の訪問に備える (k+1)
            
            # (r,c)のk回目訪問に割り当てられた(c,q)
            c_in, q_in = visit_map[(r, c, visit_k)]
            
            # s[r][c] が未定(-1)なら、これが初回訪問なので c_in で確定
            if s[r][c] == -1:
                s[r][c] = c_in
            
            # --- v5.5 核心ロジック (A と S の決定) ---
            
            # A (次色) の決定:
            # (r, c) 自身の「次の訪問 k+1」が期待する色 c_next_self
            if visit_k + 1 < w[r][c]:
                # (r,c) には次の訪問 k+1 がある
                c_next_self, q_next_self = visit_map[(r, c, visit_k + 1)]
                A = c_next_self
            else:
                # (r,c) の最後の訪問
                A = c_in # 色は変えない (または 0 でも良い)
            
            # S (次状態) の決定:
            # 移動先 (nr, nc) の「次の訪問 k'」が期待する状態 q_next_neighbor
            nr, nc = path_nodes[t+1]
            visit_k_next = visit_count[nr][nc] # (まだ加算されていない k' 回目)
            
            c_next_neighbor, q_next_neighbor = visit_map[(nr, nc, visit_k_next)]
            S = q_next_neighbor
            
            D = path_moves[t]
            
            # (c_in, q_in) の組は S 回の訪問でユニークなため、上書きの心配はない
            rules[(c_in, q_in)] = (A, S, D)

    # --- 最終目的地(K-1)の 'S' (Stay) ルール (K>1 の場合) ---
    if K > 1:
        fr, fc = TARGETS[K-1]
        visit_k = visit_count[fr][fc] # 最後の訪問 k'
        c_in, q_in = visit_map[(fr, fc, visit_k)]
        
        # 最終目的地の初期色が未定の場合 (K=2 で 1歩で着く等)
        if s[fr][fc] == -1: 
            s[fr][fc] = c_in
            
        # v5.5: 最後の訪問なので、A は適当 (c_in) で良い
        rules[(c_in, q_in)] = (c_in, 0, 'S') # 色は変えず、状態0で停止
    
    # s[r][c] == -1 のマス (一度も訪問しないマス) に色0を割り当てる
    for r in range(N):
        for c in range(N):
            if s[r][c] == -1:
                s[r][c] = 0
                
    M_final = len(rules)
    
    # --- Step E: 出力 ---
    
    # 開発合意事項: スコアを stderr に出力
    # V=K (全訪問) は達成できる前提
    final_score = C_final + Q_final
    print_score(final_score)
    
    # 1. C Q M
    print(f"{C_final} {Q_final} {M_final}")
    
    # 2. 初期盤面 s
    for r in range(N):
        print(" ".join(map(str, s[r])))
        
    # 3. 遷移規則 M
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
    # 開発規約: sys.setrecursionlimit
    # BFSの経路復元などで深くなる可能性は低いが、念のため
    sys.setrecursionlimit(2000) 
    
    if not read_input():
        return
        
    solve()

if __name__ == "__main__":
    main()