import sys
import time
import random
import math
from collections import deque

# 再帰上限の引き上げ（深い探索に備えるため）
sys.setrecursionlimit(2000)

def is_valid_col_seg(r1, r2, c, col_sum, has_H_wall):
    """
    指定された列の区間に水平方向の壁が存在しないか判定する。
    """
    if has_H_wall[r1][r2][c]:
        return False
    return (col_sum[c][r2] - col_sum[c][r1]) == (r2 - r1)

def is_valid_row_seg(r, c1, c2, row_sum, has_V_wall):
    """
    指定された行の区間に垂直方向の壁が存在しないか判定する。
    """
    if has_V_wall[r][c1][c2]:
        return False
    return (row_sum[r][c2] - row_sum[r][c1]) == (c2 - c1)

def get_transitions(u, col_sum, row_sum, has_H_wall, has_V_wall, N):
    """
    現在のマス u から移動可能なすべての遷移（操作）を列挙する。
    """
    r_A, c_A = u
    transitions = []
    
    # 1. 垂直方向の遷移（行をまたぐ移動）
    for r_B in range(N):
        if r_B == r_A:
            continue
        r_min = min(r_A, r_B)
        d = abs(r_B - r_A)
        if (col_sum[c_A][r_min + d] - col_sum[c_A][r_min]) != d:
            continue
        if has_H_wall[r_min][r_min + d][c_A]:
            continue
            
        h = 2 * d
        start_r = max(0, r_min - d + 1)
        end_r = min(r_min, N - h)
        
        for r in range(start_r, end_r + 1):
            if not has_H_wall[r][r + h][c_A] and (col_sum[c_A][r + h] - col_sum[c_A][r]) == h:
                transitions.append(((r_B, c_A), ('V', r, c_A, h, 1)))
                break
                
    # 2. 水平方向の遷移（列をまたぐ移動）
    for c_B in range(N):
        if c_B == c_A:
            continue
        c_min = min(c_A, c_B)
        d = abs(c_B - c_A)
        if (row_sum[r_A][c_min + d] - row_sum[r_A][c_min]) != d:
            continue
        if has_V_wall[r_A][c_min][c_min + d]:
            continue
            
        w = 2 * d
        start_c = max(0, c_min - d + 1)
        end_c = min(c_min, N - w)
        
        for c in range(start_c, end_c + 1):
            if not has_V_wall[r_A][c][c + w] and (row_sum[r_A][c + w] - row_sum[r_A][c]) == w:
                transitions.append(((r_A, c_B), ('H', r_A, c, 1, w)))
                break
                
    return transitions

def expand_vertical_op(r, c, h, col_sum, V, H, N):
    """
    垂直方向の操作(V)を、壁にぶつからない範囲で左右に拡張し、大きな長方形の操作にする。
    """
    c_left = c
    while c_left - 1 >= 0:
        if (col_sum[c_left - 1][r + h] - col_sum[c_left - 1][r]) != h:
            break
        ok = True
        for x in range(r, r + h - 1):
            if H[x][c_left - 1] == '1':
                ok = False
                break
        if not ok: break
        for x in range(r, r + h):
            if V[x][c_left - 1] == '1':
                ok = False
                break
        if not ok: break
        c_left -= 1
        
    c_right = c
    while c_right + 1 < N:
        if (col_sum[c_right + 1][r + h] - col_sum[c_right + 1][r]) != h:
            break
        ok = True
        for x in range(r, r + h - 1):
            if H[x][c_right + 1] == '1':
                ok = False
                break
        if not ok: break
        for x in range(r, r + h):
            if V[x][c_right] == '1':
                ok = False
                break
        if not ok: break
        c_right += 1
        
    return r, c_left, h, c_right - c_left + 1

def expand_horizontal_op(r, c, w, row_sum, V, H, N):
    """
    水平方向の操作(H)を、壁にぶつからない範囲で上下に拡張し、大きな長方形の操作にする。
    """
    r_up = r
    while r_up - 1 >= 0:
        if (row_sum[r_up - 1][c + w] - row_sum[r_up - 1][c]) != w:
            break
        ok = True
        for y in range(c, c + w - 1):
            if V[r_up - 1][y] == '1':
                ok = False
                break
        if not ok: break
        for y in range(c, c + w):
            if H[r_up - 1][y] == '1':
                ok = False
                break
        if not ok: break
        r_up -= 1
        
    r_down = r
    while r_down + 1 < N:
        if (row_sum[r_down + 1][c + w] - row_sum[r_down + 1][c]) != w:
            break
        ok = True
        for y in range(c, c + w - 1):
            if V[r_down + 1][y] == '1':
                ok = False
                break
        if not ok: break
        for y in range(c, c + w):
            if H[r_down][y] == '1':
                ok = False
                break
        if not ok: break
        r_down += 1
        
    return r_up, c, r_down - r_up + 1, w

def apply_op(op_type, r, c, h, w, pos_to_card, card_to_pos):
    """
    拡張された操作（長方形のスワップ）を盤面状態に適用し、カード位置を更新する。
    """
    if op_type == 'V':
        for x in range(h // 2):
            for y in range(w):
                cell1 = (r + x, c + y)
                cell2 = (r + h // 2 + x, c + y)
                card1, card2 = pos_to_card[cell1[0]][cell1[1]], pos_to_card[cell2[0]][cell2[1]]
                pos_to_card[cell1[0]][cell1[1]], pos_to_card[cell2[0]][cell2[1]] = card2, card1
                card_to_pos[card1], card_to_pos[card2] = cell2, cell1
    elif op_type == 'H':
        for x in range(h):
            for y in range(w // 2):
                cell1 = (r + x, c + y)
                cell2 = (r + x, c + w // 2 + y)
                card1, card2 = pos_to_card[cell1[0]][cell1[1]], pos_to_card[cell2[0]][cell2[1]]
                pos_to_card[cell1[0]][cell1[1]], pos_to_card[cell2[0]][cell2[1]] = card2, card1
                card_to_pos[card1], card_to_pos[card2] = cell2, cell1

def find_transition_path_bidirectional(start, target, col_sum, row_sum, has_H_wall, has_V_wall, N):
    """
    双方向BFSを用いて、始点から終点までの最短操作経路を探索する。
    """
    if start == target:
        return []
        
    q_f = deque([start])
    parent_f = [[None] * N for _ in range(N)]
    op_f = [[None] * N for _ in range(N)]
    parent_f[start[0]][start[1]] = (-2, -2) # 番兵
    
    q_b = deque([target])
    parent_b = [[None] * N for _ in range(N)]
    op_b = [[None] * N for _ in range(N)]
    parent_b[target[0]][target[1]] = (-2, -2) # 番兵
    
    found = False
    meeting_node = None
    
    # 探索の交差点が見つかるまで前進・後退を交互に展開
    while q_f and q_b:
        sz_f = len(q_f)
        for _ in range(sz_f):
            curr = q_f.popleft()
            for nxt, op in get_transitions(curr, col_sum, row_sum, has_H_wall, has_V_wall, N):
                nr, nc = nxt
                if parent_f[nr][nc] is None:
                    parent_f[nr][nc] = curr
                    op_f[nr][nc] = op
                    if parent_b[nr][nc] is not None:
                        meeting_node = nxt
                        found = True
                        break
                    q_f.append(nxt)
            if found: break
        if found: break
            
        sz_b = len(q_b)
        for _ in range(sz_b):
            curr = q_b.popleft()
            for nxt, op in get_transitions(curr, col_sum, row_sum, has_H_wall, has_V_wall, N):
                nr, nc = nxt
                if parent_b[nr][nc] is None:
                    parent_b[nr][nc] = curr
                    op_b[nr][nc] = op
                    if parent_f[nr][nc] is not None:
                        meeting_node = nxt
                        found = True
                        break
                    q_b.append(nxt)
            if found: break
        if found: break
            
    if meeting_node is None:
        return None
        
    # 出会った地点から経路を復元する
    path_b_to_meeting = []
    curr = meeting_node
    while curr != target:
        cr, cc = curr
        path_b_to_meeting.append(op_b[cr][cc])
        curr = parent_b[cr][cc]
    path_b_to_meeting.reverse()
    
    path_meeting_to_start = []
    curr = meeting_node
    while curr != start:
        cr, cc = curr
        path_meeting_to_start.append(op_f[cr][cc])
        curr = parent_f[cr][cc]
        
    return path_b_to_meeting + path_meeting_to_start

def is_cut_vertex_full(v, adj, in_S, S_len, N):
    """
    指定されたマス v を取り除いたとき、残りの未確定マスが分断されるか（関節点か）を判定する。
    """
    neighbors = [nxt for nxt in adj[v[0]][v[1]] if in_S[nxt[0]][nxt[1]]]
    if len(neighbors) <= 1:
        return False
        
    start = neighbors[0]
    in_S[v[0]][v[1]] = False
    
    visited_grid = [[False] * N for _ in range(N)]
    visited_grid[start[0]][start[1]] = True
    visited_count = 1
    
    q = deque([start])
    while q:
        curr = q.popleft()
        for nxt in adj[curr[0]][curr[1]]:
            if in_S[nxt[0]][nxt[1]] and not visited_grid[nxt[0]][nxt[1]]:
                visited_grid[nxt[0]][nxt[1]] = True
                visited_count += 1
                q.append(nxt)
                
    in_S[v[0]][v[1]] = True
    return visited_count != (S_len - 1)

def run_solver(preferred_order, N, initial_a, V, H, adj, has_H_wall, has_V_wall):
    """
    与えられた「マスの確定順序」に従い、貪欲法ベースで全体を揃える操作列を生成する。
    """
    # 状態の初期化
    card_to_pos = [None] * (N * N)
    pos_to_card = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            val = initial_a[r][c]
            card_to_pos[val] = (r, c)
            pos_to_card[r][c] = val
            
    S = set((r, c) for r in range(N) for c in range(N))
    in_S = [[True] * N for _ in range(N)]
    
    col_sum = [[0] * (N + 1) for _ in range(N)]
    row_sum = [[0] * (N + 1) for _ in range(N)]
    for c in range(N):
        for r in range(N):
            col_sum[c][r+1] = col_sum[c][r] + 1
    for r in range(N):
        for c in range(N):
            row_sum[r][c+1] = row_sum[r][c] + 1
            
    ops = []
    pref_idx = 0
    
    while len(S) > 1:
        # 次に確定させるべきマスを探索
        while pref_idx < len(preferred_order) and not in_S[preferred_order[pref_idx][0]][preferred_order[pref_idx][1]]:
            pref_idx += 1
            
        best_v = None
        idx = pref_idx
        while idx < len(preferred_order):
            cell = preferred_order[idx]
            # 関節点でない（分断を防ぐ）マスを選ぶ
            if in_S[cell[0]][cell[1]]:
                if not is_cut_vertex_full(cell, adj, in_S, len(S), N):
                    best_v = cell
                    break
            idx += 1
            
        if best_v is None:
            return None # 手詰まり（解なし）
            
        target_pos = card_to_pos[best_v[0] * N + best_v[1]]
        ops_in_path = find_transition_path_bidirectional(best_v, target_pos, col_sum, row_sum, has_H_wall, has_V_wall, N)
        if ops_in_path is None:
            return None # 経路なし
            
        # 経路の拡張と適用
        for op in ops_in_path:
            op_type, r, c, h, w = op
            if op_type == 'V':
                r_exp, c_exp, h_exp, w_exp = expand_vertical_op(r, c, h, col_sum, V, H, N)
            else:
                r_exp, c_exp, h_exp, w_exp = expand_horizontal_op(r, c, w, row_sum, V, H, N)
            ops.append(f"{op_type} {r_exp} {c_exp} {h_exp} {w_exp}")
            apply_op(op_type, r_exp, c_exp, h_exp, w_exp, pos_to_card, card_to_pos)
            
        S.remove(best_v)
        in_S[best_v[0]][best_v[1]] = False
        br, bc = best_v
        for r in range(br + 1, N + 1):
            col_sum[bc][r] -= 1
        for c in range(bc + 1, N + 1):
            row_sum[br][c] -= 1
            
    return ops

def generate_base_orders(N):
    """
    ヒューリスティックに有効と思われる初期の確定順序（ベース順序）を複数生成する。
    """
    orders = []
    # 1. Row T-B L-R
    orders.append([(r, c) for r in range(N) for c in range(N)])
    # 2. Row B-T L-R
    orders.append([(r, c) for r in reversed(range(N)) for c in range(N)])
    # 3. Col L-R T-B
    orders.append([(r, c) for c in range(N) for r in range(N)])
    # 4. Col R-L T-B
    orders.append([(r, c) for c in reversed(range(N)) for r in range(N)])
    # 5. Snake Row T-B L-R
    ord5 = []
    for r in range(N):
        cols = range(N) if r % 2 == 0 else reversed(range(N))
        for c in cols:
            ord5.append((r, c))
    orders.append(ord5)
    # 6. Spiral In CW from TL
    ord6 = []
    seen = [[False] * N for _ in range(N)]
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    r, c, di = 0, 0, 0
    for _ in range(N * N):
        ord6.append((r, c))
        seen[r][c] = True
        nr, nc = r + dr[di], c + dc[di]
        if 0 <= nr < N and 0 <= nc < N and not seen[nr][nc]:
            r, c = nr, nc
        else:
            di = (di + 1) % 4
            r, c = r + dr[di], c + dc[di]
    orders.append(ord6)
    return orders

def solve():
    """
    AHC068 メイン処理。入力を受け取り、焼きなまし法を用いて最適な操作列を出力する。
    """
    start_time = time.time()
    
    # ---------------------------------------------
    # 入力読み込み処理
    # ---------------------------------------------
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    a = []
    idx = 1
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        a.append(row)
        
    V = []
    for r in range(N):
        V.append(input_data[idx])
        idx += 1
        
    H = []
    for r in range(N-1):
        H.append(input_data[idx])
        idx += 1
        
    # 壁の存在確認配列を構築
    has_H_wall = [[[False] * N for _ in range(N + 1)] for _ in range(N)]
    for c in range(N):
        for r1 in range(N):
            wall = False
            for r2 in range(r1 + 1, N + 1):
                if r2 - 2 >= r1 and H[r2 - 2][c] == '1':
                    wall = True
                has_H_wall[r1][r2][c] = wall
                
    has_V_wall = [[[False] * (N + 1) for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c1 in range(N):
            wall = False
            for c2 in range(c1 + 1, N + 1):
                if c2 - 2 >= c1 and V[r][c2 - 2] == '1':
                    wall = True
                has_V_wall[r][c1][c2] = wall
                
    # 連結性チェック用の隣接リスト
    adj = [[[] for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if c + 1 < N and V[r][c] == '0':
                adj[r][c].append((r, c+1))
                adj[r][c+1].append((r, c))
            if r + 1 < N and H[r][c] == '0':
                adj[r][c].append((r+1, c))
                adj[r+1][c].append((r, c))
                
    # ---------------------------------------------
    # Phase 1: ベース順序の評価
    # ---------------------------------------------
    base_orders = generate_base_orders(N)
    best_ops = None
    best_ops_len = float('inf')
    best_order = None
    
    for order in base_orders:
        ops = run_solver(order, N, a, V, H, adj, has_H_wall, has_V_wall)
        if ops is not None and len(ops) < best_ops_len:
            best_ops_len = len(ops)
            best_ops = ops
            best_order = list(order)

    # ---------------------------------------------
    # Phase 2: 焼きなまし法 (Simulated Annealing)
    # ---------------------------------------------
    if best_order is not None:
        rng = random.Random(42)
        current_order = list(best_order)
        current_score = best_ops_len
        
        # --- 焼きなまし法の核心部: 温度管理とスケジューリング ---
        TIME_LIMIT = 1.72 # 実行時間制限2.0秒に対し、余裕を持たせた終了時刻
        START_TEMP = 10.0 # 序盤は数手(10手前後)の悪化を許容する
        END_TEMP = 0.1
        
        # 【修正箇所】ループ開始前に初期温度をセットしておく
        current_temp = START_TEMP
        
        iter_count = 0
        while True:
            iter_count += 1
            if iter_count % 10 == 0: # 頻繁な時刻取得によるオーバーヘッドを防ぐ
                now_time = time.time()
                elapsed = now_time - start_time
                if elapsed >= TIME_LIMIT:
                    break
                # 残り時間に応じて温度を計算し、更新する
                progress = elapsed / TIME_LIMIT
                current_temp = START_TEMP * ((END_TEMP / START_TEMP) ** progress)
            
            # --- 焼きなまし法の核心部: 近傍操作 ---
            new_order = list(current_order)
            operation_type = rng.random()
            if operation_type < 0.7:
                # 70%の確率で 2点スワップ
                idx1 = rng.randint(0, len(new_order) - 1)
                idx2 = rng.randint(0, len(new_order) - 1)
                new_order[idx1], new_order[idx2] = new_order[idx2], new_order[idx1]
            else:
                # 30%の確率で 区間反転 (2-opt的アプローチ)
                idx1 = rng.randint(0, len(new_order) - 2)
                idx2 = rng.randint(idx1 + 1, len(new_order) - 1)
                new_order[idx1:idx2+1] = reversed(new_order[idx1:idx2+1])
                
            # 新しい状態でのスコア計算 (run_solver関数を呼び出す)
            ops = run_solver(new_order, N, a, V, H, adj, has_H_wall, has_V_wall)
            new_score = len(ops) if ops is not None else float('inf')
            
            # --- 焼きなまし法の核心部: 遷移の受容判定 ---
            if new_score <= current_score:
                # スコアが改善、または同値なら確定で受け入れる
                current_order = new_order
                current_score = new_score
                # 暫定ベストの更新
                if new_score < best_ops_len:
                    best_ops_len = new_score
                    best_ops = ops
            else:
                # 悪化した場合でも、確率で受け入れる (Metropolis criterion)
                # current_tempが初期化されているので、ここでエラーは起きない
                prob = math.exp((current_score - new_score) / current_temp)
                if rng.random() < prob:
                    current_order = new_order
                    current_score = new_score

    # 万が一すべて失敗した場合のフォールバック
    if best_ops is None:
        best_ops = run_solver(base_orders[0], N, a, V, H, adj, has_H_wall, has_V_wall)
            
    # 出力
    for op in best_ops:
        print(op)

if __name__ == '__main__':
    solve()