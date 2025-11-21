import sys
import time
import math
from collections import deque

# --- グローバル変数 (入力値) ---
N: int = 0
K: int = 0
T: int = 0
VWALLS: list[list[int]] = []
HWALLS: list[list[int]] = []
TARGETS: list[tuple[int, int]] = []

# 移動方向 (dr, dc, D)
DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}
# 逆引き用
REV_DIRECTIONS = {v: k for k, v in DIRECTIONS.items()}


def load_input():
    """
    標準入力から問題の入力を読み込み、グローバル変数に格納する。
    (v2 と同一)
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    
    try:
        N, K, T = map(int, sys.stdin.readline().split())
        VWALLS = [list(map(int, list(sys.stdin.readline().strip()))) for _ in range(N)]
        HWALLS = [list(map(int, list(sys.stdin.readline().strip()))) for _ in range(N - 1)]
        TARGETS = []
        for _ in range(K):
            r, c = map(int, sys.stdin.readline().split())
            TARGETS.append((r, c))
    except Exception as e:
        print(f"入力の読み込み中にエラー: {e}", file=sys.stderr)
        sys.exit(1)


class BfsSolver:
    """
    壁情報を考慮したBFS（幅優先探索）を実行し、2点間の最短経路を計算するクラス。
    (v2 と同一)
    """
    
    def __init__(self, n: int, v_walls: list[list[int]], h_walls: list[list[int]]):
        self.N = n
        self.v_walls = v_walls
        self.h_walls = h_walls
        self.cache = {} # v4: 実行時間短縮のため、v3のキャッシュ機能を採用

    def _is_valid(self, r: int, c: int) -> bool:
        return 0 <= r < self.N and 0 <= c < self.N

    def _can_move(self, r: int, c: int, dr: int, dc: int) -> bool:
        nr, nc = r + dr, c + dc
        if not self._is_valid(nr, nc): return False
        if dr == -1: return self.h_walls[nr][c] == 0
        if dr == 1:  return self.h_walls[r][c] == 0
        if dc == -1: return self.v_walls[r][nc] == 0
        if dc == 1:  return self.v_walls[r][c] == 0
        return False

    def solve(self, start_r: int, start_c: int, goal_r: int, goal_c: int) -> tuple[list[tuple[int, int]], list[str]]:
        """
        BFSを実行し、スタートからゴールまでの最短経路を返す。(キャッシュ利用)
        """
        start_node = (start_r, start_c)
        goal_node = (goal_r, goal_c)
        
        if (start_node, goal_node) in self.cache:
            return self.cache[(start_node, goal_node)]
        
        queue = deque([(start_r, start_c)])
        prev = { (start_r, start_c): (None, None, None) }
        found = False
        
        while queue:
            r, c = queue.popleft()
            if r == goal_r and c == goal_c:
                found = True
                break
            for move_char, (dr, dc) in DIRECTIONS.items():
                if self._can_move(r, c, dr, dc):
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in prev:
                        prev[(nr, nc)] = (r, c, move_char)
                        queue.append((nr, nc))
                        
        if not found:
            self.cache[(start_node, goal_node)] = ([], [])
            return [], []

        path_nodes = []
        path_moves = []
        curr_r, curr_c = goal_r, goal_c
        while (curr_r, curr_c) != (start_r, start_c):
            path_nodes.append((curr_r, curr_c))
            pr, pc, move = prev[(curr_r, curr_c)]
            path_moves.append(move)
            curr_r, curr_c = pr, pc
        path_nodes.append((start_r, start_c))
        path_nodes.reverse()
        path_moves.reverse()
        
        self.cache[(start_node, goal_node)] = (path_nodes, path_moves)
        return path_nodes, path_moves


def run_ffd_bin_packing(
    Q_capacity: int, 
    w: list[list[int]], 
    items: list[tuple[int, int, int]], 
    start_item_tuple: tuple[int, int, int]
) -> tuple[int, list[list[int]], list[list[int]]]:
    """
    v4 核心部: FFD（First Fit Decreasing）ビンパッキングを実行する。
    v2 (バグ修正版) のロジックを関数として分離。

    Args:
        Q_capacity (int): ビンの容量 (候補となるQ)
        w (list[list[int]]): 全マスの重み配列
        items (list): ソート済みのアイテムリスト (w, r, c)
        start_item_tuple (tuple): スタート地点のアイテム (w, r, c)

    Returns:
        tuple: (C_final, s, q_offset)
            C_final (int): このQで必要になった色数
            s (list[list[int]]): 割り当てられた色ID
            q_offset (list[list[int]]): 割り当てられた状態オフセット
    """
    
    s = [[-1] * N for _ in range(N)]
    q_offset = [[0] * N for _ in range(N)]
    
    # items はソート済みのコピーを受け取ることを想定
    items_copy = list(items)
    
    color_bins_weight = []
    C_final = 0
    
    # 1. スタート地点 (TARGETS[0]) を最優先で「色 0」に割り当てる
    start_w, start_r, start_c = start_item_tuple
    
    if start_w > 0:
        s[start_r][start_c] = 0
        q_offset[start_r][start_c] = 0
        color_bins_weight.append(start_w)
        C_final = 1
        
        try:
            items_copy.remove(start_item_tuple)
        except ValueError:
            pass
    
    # 2. 残りのアイテムで FFD を実行
    for weight, r, c in items_copy:
        assigned = False
        for c_id in range(C_final):
            if color_bins_weight[c_id] + weight <= Q_capacity:
                s[r][c] = c_id
                q_offset[r][c] = color_bins_weight[c_id]
                color_bins_weight[c_id] += weight
                assigned = True
                break
        if not assigned:
            new_c_id = len(color_bins_weight)
            s[r][c] = new_c_id
            q_offset[r][c] = 0
            color_bins_weight.append(weight)
            C_final += 1

    # 3. 未訪問マスを色0に
    for r in range(N):
        for c in range(N):
            if s[r][c] == -1:
                s[r][c] = 0
                
    if C_final == 0:
        C_final = 1
        if s[start_r][start_c] == -1:
             s[start_r][start_c] = 0
             
    return C_final, s, q_offset


def solve():
    """
    「v4: 最適 Q 探索」アルゴリズムのメインロジックを実行する。
    """
    global N, K, T, TARGETS, VWALLS, HWALLS # グローバル変数を参照
    start_time = time.time()
    
    # --- Step A: 経路計算と w[i][j] の確定 (v2流用) ---
    
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    
    w = [[0] * N for _ in range(N)]
    all_paths_info = []
    
    for k in range(K - 1):
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        path_nodes, path_moves = bfs_solver.solve(sr, sc, gr, gc)
        if not path_nodes:
            print(f"エラー: 経路 {k} -> {k+1} が見つかりません", file=sys.stderr)
            return
        all_paths_info.append((path_nodes, path_moves))
        for i in range(len(path_nodes) - 1):
            r, c = path_nodes[i]
            w[r][c] += 1
            
    last_r, last_c = TARGETS[K-1]
    w[last_r][last_c] += 1

    # --- v4 核心部: ビンパッキング用の事前計算 ---
    
    max_w = 0
    sum_w = 0
    items = [] # (重み, 行, 列)
    for r in range(N):
        for c in range(N):
            if w[r][c] > 0:
                max_w = max(max_w, w[r][c])
                sum_w += w[r][c]
                items.append((w[r][c], r, c))

    # FFD のため、重みの降順でソート (1回だけ行う)
    items.sort(key=lambda x: x[0], reverse=True)
    
    start_r, start_c = TARGETS[0]
    start_w = w[start_r][start_c]
    start_item_tuple = (start_w, start_r, start_c)

    
    # --- Step B: 最適な Q の探索 ---
    
    Q_min = max(1, max_w) # Qの絶対的な下限
    
    if sum_w == 0: # K=1 などの特殊ケース
        Q_ideal = 1
    else:
        # C+Q が最小になるのは Q = sqrt(sum_w) の周辺
        Q_ideal = max(Q_min, int(math.sqrt(sum_w) + 0.5))

    # Q_min と Q_ideal 周辺を探索する
    # 実行時間 (1.8s) に余裕があるため、広めに探索 (例: ±30)
    search_range_start = max(Q_min, Q_ideal - 30)
    search_range_end = Q_ideal + 30
    
    search_candidates = set(range(search_range_start, search_range_end + 1))
    search_candidates.add(Q_min) # 下限値は必ず試す
    
    best_score = float('inf')
    best_Q = -1
    best_C = -1
    best_s = None
    best_q_offset = None

    for Q_candidate in sorted(list(search_candidates)):
        
        # 実行時間が 1.7秒 を超えたら探索を打ち切る
        if time.time() - start_time > 1.7:
            break
        
        # 候補 Q でビンパッキングを実行
        C_candidate, s_candidate, q_offset_candidate = run_ffd_bin_packing(
            Q_candidate, w, items, start_item_tuple
        )
        
        score = C_candidate + Q_candidate
        
        if score < best_score:
            best_score = score
            best_Q = Q_candidate
            best_C = C_candidate
            best_s = s_candidate
            best_q_offset = q_offset_candidate

    # --- Step C: 遷移規則 M の生成 (v2流用) ---
    # best_s, best_q_offset を使ってルール生成
    
    Q_final = best_Q
    C_final = best_C
    s = best_s
    q_offset = best_q_offset
    
    visit_count = [[0] * N for _ in range(N)]
    rules = {}
    
    for path_nodes, path_moves in all_paths_info:
        path_len = len(path_moves)
        for t in range(path_len):
            r, c = path_nodes[t]
            c_now = s[r][c]
            q_now = q_offset[r][c] + visit_count[r][c]
            visit_count[r][c] += 1
            
            A = c_now
            D = path_moves[t]
            
            nr, nc = path_nodes[t+1]
            S = q_offset[nr][nc] + visit_count[nr][nc]
            
            rules[(c_now, q_now)] = (A, S, D)

    fr, fc = TARGETS[K-1]
    c_final_pos = s[fr][fc]
    q_final_pos = q_offset[fr][fc] + visit_count[fr][fc]
    rules[(c_final_pos, q_final_pos)] = (c_final_pos, 0, 'S')
    
    M_final = len(rules)

    # --- Step D: 出力 (v2流用) ---
    
    final_score = C_final + Q_final
    print(final_score, file=sys.stderr)
    
    print(f"{C_final} {Q_final} {M_final}")
    
    for r in range(N):
        print(" ".join(map(str, s[r])))
        
    for (c, q), (A, S, D) in rules.items():
        print(f"{c} {q} {A} {S} {D}")


def main():
    """
    メイン処理。入力を読み込み、解法を実行する。
    """
    global sys
    load_input()
    if N == 0:
        print("入力が読み込めませんでした。", file=sys.stderr)
        return
    solve()

if __name__ == "__main__":
    main()