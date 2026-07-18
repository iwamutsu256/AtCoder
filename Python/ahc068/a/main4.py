import sys
import time
import random
from collections import deque

# Increase recursion limit just in case
sys.setrecursionlimit(2000)

def is_valid_col_seg(r1, r2, c, col_sum, has_H_wall):
    if has_H_wall[r1][r2][c]:
        return False
    return (col_sum[c][r2] - col_sum[c][r1]) == (r2 - r1)

def is_valid_row_seg(r, c1, c2, row_sum, has_V_wall):
    if has_V_wall[r][c1][c2]:
        return False
    return (row_sum[r][c2] - row_sum[r][c1]) == (c2 - c1)

def get_transitions(u, col_sum, row_sum, has_H_wall, has_V_wall, N):
    r_A, c_A = u
    transitions = []
    
    # 1. Vertical transitions: swap (r_A, c_A) with (r_B, c_A)
    for r_B in range(N):
        if r_B == r_A:
            continue
        r_min = min(r_A, r_B)
        d = abs(r_B - r_A)
        # Fast prefix-sum check
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
                
    # 2. Horizontal transitions: swap (r_A, c_A) with (r_A, c_B)
    for c_B in range(N):
        if c_B == c_A:
            continue
        c_min = min(c_A, c_B)
        d = abs(c_B - c_A)
        # Fast prefix-sum check
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
    c_left = c
    while c_left - 1 >= 0:
        if (col_sum[c_left - 1][r + h] - col_sum[c_left - 1][r]) != h:
            break
        ok = True
        for x in range(r, r + h - 1):
            if H[x][c_left - 1] == '1':
                ok = False
                break
        if not ok:
            break
        for x in range(r, r + h):
            if V[x][c_left - 1] == '1':
                ok = False
                break
        if not ok:
            break
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
        if not ok:
            break
        for x in range(r, r + h):
            if V[x][c_right] == '1':
                ok = False
                break
        if not ok:
            break
        c_right += 1
        
    return r, c_left, h, c_right - c_left + 1

def expand_horizontal_op(r, c, w, row_sum, V, H, N):
    r_up = r
    while r_up - 1 >= 0:
        if (row_sum[r_up - 1][c + w] - row_sum[r_up - 1][c]) != w:
            break
        ok = True
        for y in range(c, c + w - 1):
            if V[r_up - 1][y] == '1':
                ok = False
                break
        if not ok:
            break
        for y in range(c, c + w):
            if H[r_up - 1][y] == '1':
                ok = False
                break
        if not ok:
            break
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
        if not ok:
            break
        for y in range(c, c + w):
            if H[r_down][y] == '1':
                ok = False
                break
        if not ok:
            break
        r_down += 1
        
    return r_up, c, r_down - r_up + 1, w

def apply_op(op_type, r, c, h, w, pos_to_card, card_to_pos):
    if op_type == 'V':
        for x in range(h // 2):
            for y in range(w):
                cell1 = (r + x, c + y)
                cell2 = (r + h // 2 + x, c + y)
                
                card1 = pos_to_card[cell1[0]][cell1[1]]
                card2 = pos_to_card[cell2[0]][cell2[1]]
                
                pos_to_card[cell1[0]][cell1[1]] = card2
                pos_to_card[cell2[0]][cell2[1]] = card1
                
                card_to_pos[card1] = cell2
                card_to_pos[card2] = cell1
    elif op_type == 'H':
        for x in range(h):
            for y in range(w // 2):
                cell1 = (r + x, c + y)
                cell2 = (r + x, c + w // 2 + y)
                
                card1 = pos_to_card[cell1[0]][cell1[1]]
                card2 = pos_to_card[cell2[0]][cell2[1]]
                
                pos_to_card[cell1[0]][cell1[1]] = card2
                pos_to_card[cell2[0]][cell2[1]] = card1
                
                card_to_pos[card1] = cell2
                card_to_pos[card2] = cell1

def find_transition_path_bidirectional(start, target, col_sum, row_sum, has_H_wall, has_V_wall, N):
    if start == target:
        return []
        
    q_f = deque([start])
    parent_f = [[None] * N for _ in range(N)]
    op_f = [[None] * N for _ in range(N)]
    parent_f[start[0]][start[1]] = (-2, -2) # Sentinel
    
    q_b = deque([target])
    parent_b = [[None] * N for _ in range(N)]
    op_b = [[None] * N for _ in range(N)]
    parent_b[target[0]][target[1]] = (-2, -2) # Sentinel
    
    found = False
    meeting_node = None
    
    while q_f and q_b:
        sz_f = len(q_f)
        for _ in range(sz_f):
            curr = q_f.popleft()
            transitions = get_transitions(curr, col_sum, row_sum, has_H_wall, has_V_wall, N)
            for nxt, op in transitions:
                nr, nc = nxt
                if parent_f[nr][nc] is None:
                    parent_f[nr][nc] = curr
                    op_f[nr][nc] = op
                    if parent_b[nr][nc] is not None:
                        meeting_node = nxt
                        found = True
                        break
                    q_f.append(nxt)
            if found:
                break
        if found:
            break
            
        sz_b = len(q_b)
        for _ in range(sz_b):
            curr = q_b.popleft()
            transitions = get_transitions(curr, col_sum, row_sum, has_H_wall, has_V_wall, N)
            for nxt, op in transitions:
                nr, nc = nxt
                if parent_b[nr][nc] is None:
                    parent_b[nr][nc] = curr
                    op_b[nr][nc] = op
                    if parent_f[nr][nc] is not None:
                        meeting_node = nxt
                        found = True
                        break
                    q_b.append(nxt)
            if found:
                break
        if found:
            break
            
    if meeting_node is None:
        return None
        
    # Reconstruct path from target to start
    # 1. From target to meeting_node
    path_b_to_meeting = []
    curr = meeting_node
    while curr != target:
        cr, cc = curr
        parent = parent_b[cr][cc]
        op = op_b[cr][cc]
        path_b_to_meeting.append(op)
        curr = parent
    path_b_to_meeting.reverse()
    
    # 2. From meeting_node to start
    path_meeting_to_start = []
    curr = meeting_node
    while curr != start:
        cr, cc = curr
        parent = parent_f[cr][cc]
        op = op_f[cr][cc]
        path_meeting_to_start.append(op)
        curr = parent
        
    return path_b_to_meeting + path_meeting_to_start

def is_cut_vertex_full(v, adj, in_S, S_len, N):
    neighbors = [nxt for nxt in adj[v[0]][v[1]] if in_S[nxt[0]][nxt[1]]]
    deg = len(neighbors)
    if deg <= 1:
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
        while pref_idx < len(preferred_order) and not in_S[preferred_order[pref_idx][0]][preferred_order[pref_idx][1]]:
            pref_idx += 1
            
        best_v = None
        idx = pref_idx
        while idx < len(preferred_order):
            cell = preferred_order[idx]
            if in_S[cell[0]][cell[1]]:
                if not is_cut_vertex_full(cell, adj, in_S, len(S), N):
                    best_v = cell
                    break
            idx += 1
            
        if best_v is None:
            return None
            
        target_pos = card_to_pos[best_v[0] * N + best_v[1]]
        ops_in_path = find_transition_path_bidirectional(best_v, target_pos, col_sum, row_sum, has_H_wall, has_V_wall, N)
        if ops_in_path is None:
            return None
            
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

def generate_random_shrinking_order(N, rng):
    r_min, r_max = 0, N - 1
    c_min, c_max = 0, N - 1
    
    order = []
    while r_min <= r_max and c_min <= c_max:
        choices = []
        if r_min <= r_max:
            choices.append(0) # Top
            choices.append(1) # Bottom
        if c_min <= c_max:
            choices.append(2) # Left
            choices.append(3) # Right
            
        choice = rng.choice(choices)
        if choice == 0:
            cols = list(range(c_min, c_max + 1))
            if rng.choice([True, False]):
                cols.reverse()
            for c in cols:
                order.append((r_min, c))
            r_min += 1
        elif choice == 1:
            cols = list(range(c_min, c_max + 1))
            if rng.choice([True, False]):
                cols.reverse()
            for c in cols:
                order.append((r_max, c))
            r_max -= 1
        elif choice == 2:
            rows = list(range(r_min, r_max + 1))
            if rng.choice([True, False]):
                rows.reverse()
            for r in rows:
                order.append((r, c_min))
            c_min += 1
        elif choice == 3:
            rows = list(range(r_min, r_max + 1))
            if rng.choice([True, False]):
                rows.reverse()
            for r in rows:
                order.append((r, c_max))
            c_max -= 1
            
    return order

def generate_base_orders(N):
    orders = []
    # 1. Row T-B L-R
    orders.append([(r, c) for r in range(N) for c in range(N)])
    # 2. Row B-T L-R
    orders.append([(r, c) for r in reversed(range(N)) for c in range(N)])
    # 3. Col L-R T-B
    orders.append([(r, c) for c in range(N) for r in range(N)])
    return orders

def solve():
    start_time = time.time()
    
    # Read all input from stdin
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
                
    adj = [[[] for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if c + 1 < N and V[r][c] == '0':
                adj[r][c].append((r, c+1))
                adj[r][c+1].append((r, c))
            if r + 1 < N and H[r][c] == '0':
                adj[r][c].append((r+1, c))
                adj[r+1][c].append((r, c))
                
    best_ops = None
    best_ops_len = 999999
    
    # Phase 1: Evaluate top 3 structured base orders
    base_orders = generate_base_orders(N)
    for order in base_orders:
        if time.time() - start_time >= 1.85:
            break
        ops = run_solver(order, N, a, V, H, adj, has_H_wall, has_V_wall)
        if ops is not None and len(ops) < best_ops_len:
            best_ops_len = len(ops)
            best_ops = ops
            
    # Phase 2: Generate and evaluate randomized shrinking orders
    rng = random.Random(42)
    while time.time() - start_time < 1.85:
        order = generate_random_shrinking_order(N, rng)
        ops = run_solver(order, N, a, V, H, adj, has_H_wall, has_V_wall)
        if ops is not None and len(ops) < best_ops_len:
            best_ops_len = len(ops)
            best_ops = ops
            
    # Fallback
    if best_ops is None:
        best_ops = run_solver(base_orders[0], N, a, V, H, adj, has_H_wall, has_V_wall)
            
    for op in best_ops:
        print(op)

if __name__ == '__main__':
    solve()
