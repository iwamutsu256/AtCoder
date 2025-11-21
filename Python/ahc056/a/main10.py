import sys
from collections import deque
import time

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
    """
    global N, K, T, VWALLS, HWALLS, TARGETS
    
    try:
        N, K, T = map(int, sys.stdin.readline().split())
        
        VWALLS = []
        for _ in range(N):
            VWALLS.append(list(map(int, list(sys.stdin.readline().strip()))))
            
        HWALLS = []
        for _ in range(N - 1):
            HWALLS.append(list(map(int, list(sys.stdin.readline().strip()))))
            
        TARGETS = []
        for _ in range(K):
            r, c = map(int, sys.stdin.readline().split())
            TARGETS.append((r, c))
            
    except EOFError:
        pass
    except Exception as e:
        print(f"入力の読み込み中にエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


class BfsSolver:
    """
    壁情報を考慮したBFS（幅優先探索）を実行し、2点間の最短経路を計算するクラス。
    """
    
    def __init__(self, n: int, v_walls: list[list[int]], h_walls: list[list[int]]):
        """
        BfsSolverを初期化する。

        Args:
            n (int): グリッドのサイズ (N)
            v_walls (list[list[int]]): 垂直方向の壁情報
            h_walls (list[list[int]]): 水平方向の壁情報
        """
        self.N = n
        self.v_walls = v_walls
        self.h_walls = h_walls

    def _is_valid(self, r: int, c: int) -> bool:
        """指定されたマス (r, c) がグリッド内かどうかを判定する。"""
        return 0 <= r < self.N and 0 <= c < self.N

    def _can_move(self, r: int, c: int, dr: int, dc: int) -> bool:
        """
        マス (r, c) から (r+dr, c+dc) へ壁を考慮して移動可能か判定する。
        
        Args:
            r (int): 現在の行
            c (int): 現在の列
            dr (int): 行の移動量
            dc (int): 列の移動量

        Returns:
            bool: 移動可能なら True
        """
        nr, nc = r + dr, c + dc
        
        if not self._is_valid(nr, nc):
            return False
        
        if dr == -1: # U
            return self.h_walls[nr][c] == 0
        if dr == 1:  # D
            return self.h_walls[r][c] == 0
        if dc == -1: # L
            return self.v_walls[r][nc] == 0
        if dc == 1:  # R
            return self.v_walls[r][c] == 0
            
        return False # dr=0, dc=0 (Stay) は考慮しない

    def solve(self, start_r: int, start_c: int, goal_r: int, goal_c: int) -> tuple[list[tuple[int, int]], list[str]]:
        """
        BFSを実行し、スタートからゴールまでの最短経路（マスのリストと移動方向のリスト）を返す。

        Args:
            start_r (int): スタート行
            start_c (int): スタート列
            goal_r (int): ゴール行
            goal_c (int): ゴール列

        Returns:
            tuple[list[tuple[int, int]], list[str]]: 
                (path_nodes, path_moves)
                path_nodes: (sr, sc) から (gr, gc) までのマス座標のリスト
                path_moves: path_nodes[i] から path_nodes[i+1] へ移動するための方向 ('U', 'D', 'L', 'R') のリスト
        """
        
        queue = deque([(start_r, start_c)])
        # prev[ (r, c) ] = (pr, pc, move) : (pr, pc) から move して (r, c) に来た
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
            # 到達不可能なケース (問題設定上ありえないが念のため)
            return [], []

        # --- 経路の復元 ---
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
        
        return path_nodes, path_moves


def solve():
    """
    「v2: ビンパッキング」アルゴリズムのメインロジックを実行する。
    """
    start_time = time.time()
    
    # --- Step A: 経路計算と w[i][j] の確定 ---
    
    bfs_solver = BfsSolver(N, VWALLS, HWALLS)
    
    # w[i][j]: マス(i,j)が全経路で通過される回数（重み）
    w = [[0] * N for _ in range(N)]
    
    # all_paths_info: (path_nodes, path_moves) のリスト
    all_paths_info = []
    
    # K-1本の経路を計算
    for k in range(K - 1):
        sr, sc = TARGETS[k]
        gr, gc = TARGETS[k+1]
        
        path_nodes, path_moves = bfs_solver.solve(sr, sc, gr, gc)
        
        if not path_nodes:
            print(f"エラー: 経路 {k} -> {k+1} が見つかりません", file=sys.stderr)
            return

        all_paths_info.append((path_nodes, path_moves))
        
        # スタート地点(k) から ゴール(k+1) の手前までが w[i][j] のカウント対象
        # (ゴール地点(k+1)は、次の経路のスタート地点としてカウントされるため)
        for i in range(len(path_nodes) - 1):
            r, c = path_nodes[i]
            w[r][c] += 1
            
    # 最後の目的地(K-1)の分を1回カウント
    last_r, last_c = TARGETS[K-1]
    w[last_r][last_c] += 1

    
    # --- Step B: Q の決定と C の計算 (ビンパッキング) ---

    max_w = 0
    for r in range(N):
        for c in range(N):
            max_w = max(max_w, w[r][c])
            
    # Q_final: 必要な状態数 = マス訪問回数の最大値
    Q_final = max(1, max_w)
    
    # s[i][j]: マス(i,j)に割り当てる色ID
    s = [[-1] * N for _ in range(N)]
    # q_offset[i][j]: マス(i,j)が使用する状態qの開始オフセット
    q_offset = [[0] * N for _ in range(N)]
    
    # ビンパッキングするアイテム (重み > 0 のマス)
    items = []
    for r in range(N):
        for c in range(N):
            if w[r][c] > 0:
                # (重み, 行, 列)
                items.append((w[r][c], r, c))
                
    # FFD (First Fit Decreasing) のため、重みの降順でソート
    items.sort(key=lambda x: x[0], reverse=True)
    
    # color_bins_weight[c_id] = 色 c_id が現在使用している重み(状態数)
    color_bins_weight = []
    C_final = 0 # 最終的な色数
    
    # --- 【バグ修正】 核心部: 貪欲ビンパッキング (FFD) ---
    
    # ロボットは必ず (c, q) = (s[T[0]], 0) でスタートする。
    # したがって、スタート地点 T[0] = (sr, sc) は、
    # 訪問回数 w > 0 の場合、必ず q_offset = 0 に割り当てる必要がある。
    
    start_r, start_c = TARGETS[0]
    start_w = w[start_r][start_c]
    
    # 1. スタート地点 (TARGETS[0]) を最優先で「色 0」に割り当てる
    if start_w > 0:
        s[start_r][start_c] = 0
        q_offset[start_r][start_c] = 0
        color_bins_weight.append(start_w) # 色 0 の重み
        C_final = 1
        
        # items リストからスタート地点を安全に削除する
        # (w, r, c) タプルで比較
        start_item_tuple = (start_w, start_r, start_c)
        try:
            items.remove(start_item_tuple)
        except ValueError:
            # w > 0 なのに items にないのは稀だが、ロジック上はあり得る
            print(f"警告: スタートアイテム {start_item_tuple} が items に見つかりません", file=sys.stderr)
            pass
    
    # 2. スタート地点を除く残りのアイテムで FFD を実行
    for weight, r, c in items:
        assigned = False
        
        # 既存の色(ビン)に詰められるか探す (First Fit)
        # C_final はビンの総数
        for c_id in range(C_final):
            if color_bins_weight[c_id] + weight <= Q_final:
                s[r][c] = c_id
                q_offset[r][c] = color_bins_weight[c_id]
                color_bins_weight[c_id] += weight
                assigned = True
                break
                
        # 詰められるビンがなければ、新しい色(ビン)を追加
        if not assigned:
            new_c_id = len(color_bins_weight) # C_final と同じ
            s[r][c] = new_c_id
            q_offset[r][c] = 0 # 新しいビンのためオフセットは0
            color_bins_weight.append(weight)
            C_final += 1 # 新しい色を追加したので C_final を増やす

    # C_final: 最終的に使用した色(ビン)の数
    # C_final = len(color_bins_weight) # FFD 中に C_final を更新するよう変更
    
    # --- w[i][j] == 0 (未訪問) のマスを、色0に割り当てる ---
    # (色0が使われていなくても、0埋めすればOK)
    for r in range(N):
        for c in range(N):
            if s[r][c] == -1:
                s[r][c] = 0
                
    if C_final == 0: # 全マス未訪問の特殊ケース (K=1 など)
        C_final = 1
        if s[start_r][start_c] == -1: # K=1 で T[0] が w=0 の場合
             s[start_r][start_c] = 0


    # --- Step C: 遷移規則 M の生成 ---

    # visit_count[i][j]: シミュレーション中にマス(i,j)を訪問した回数
    visit_count = [[0] * N for _ in range(N)]
    
    # rules[(c, q)] = (A, S, D)
    rules = {}
    
    # --- 核心部: 全経路シミュレーションによるルール生成 ---
    for path_nodes, path_moves in all_paths_info:
        
        path_len = len(path_moves)
        for t in range(path_len):
            # --- 現在の(c, q)を決定 ---
            r, c = path_nodes[t]
            c_now = s[r][c]
            # (オフセット + このマスでの訪問回数) でユニークな状態qを計算
            q_now = q_offset[r][c] + visit_count[r][c]
            
            # この(c, q)は処理したので、訪問回数を増やす
            visit_count[r][c] += 1
            
            # --- 次の(A, S, D)を決定 ---
            A = c_now # 色は変更しない
            D = path_moves[t]
            
            # --- 次状態 S の決定 ---
            # 移動先のマス (nr, nc) が次に使うべき状態q
            nr, nc = path_nodes[t+1]
            S = q_offset[nr][nc] + visit_count[nr][nc]
            
            # ルールが重複することはないはず (アルゴリズムの前提)
            rules[(c_now, q_now)] = (A, S, D)

    # --- 核心部: 最終目的地(K-1)の 'S' (Stay) ルール ---
    # 最後の経路のゴール = 最終目的地
    fr, fc = TARGETS[K-1]
    
    # 最終目的地に到着した時の (c, q)
    c_final_pos = s[fr][fc]
    q_final_pos = q_offset[fr][fc] + visit_count[fr][fc]
    
    # (c, q) に遭遇したら、色を変えず(A)、状態を0(S)にし、停止(D='S')
    rules[(c_final_pos, q_final_pos)] = (c_final_pos, 0, 'S')
    
    M_final = len(rules)

    
    # --- Step D: 出力 ---
    
    # 開発合意事項(stderrへのスコア出力)
    # このアルゴリズムは V=K を前提としている
    final_score = C_final + Q_final
    print(final_score, file=sys.stderr)
    
    # 回答本体 (stdout)
    print(f"{C_final} {Q_final} {M_final}")
    
    for r in range(N):
        print(" ".join(map(str, s[r])))
        
    for (c, q), (A, S, D) in rules.items():
        print(f"{c} {q} {A} {S} {D}")
        
    # デバッグ用実行時間
    # end_time = time.time()
    # print(f"Time: {end_time - start_time:.4f} sec", file=sys.stderr)


def main():
    """
    メイン処理。入力を読み込み、解法を実行する。
    """
    # 開発合意事項: stderr出力のため、sysモジュールは必須
    global sys
    
    load_input()
    
    if N == 0:
        print("入力が読み込めませんでした。", file=sys.stderr)
        return
        
    solve()

if __name__ == "__main__":
    main()