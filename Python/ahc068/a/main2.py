import sys
from collections import deque

# Increase recursion limit just in case
sys.setrecursionlimit(2000)

def estimate_transition_dist(v, target_pos, col_sum, row_sum, has_H_wall, has_V_wall, in_S, N):
    if v == target_pos:
        return 0
    vr, vc = v
    tr, tc = target_pos
    
    d_man = abs(vr - tr) + abs(vc - tc)
    
    if vr == tr:
        c_min = min(vc, tc)
        d = abs(tc - vc)
        if not has_V_wall[vr][c_min][c_min + d]:
            w = 2 * d
            start_c = max(0, c_min - d + 1)
            end_c = min(c_min, N - w)
            for c in range(start_c, end_c + 1):
                if not has_V_wall[vr][c][c + w] and (row_sum[vr][c + w] - row_sum[vr][c]) == w:
                    return 1
    elif vc == tc:
        r_min = min(vr, tr)
        d = abs(tr - vr)
        if not has_H_wall[r_min][r_min + d][vc]:
            h = 2 * d
            start_r = max(0, r_min - d + 1)
            end_r = min(r_min, N - h)
            for r in range(start_r, end_r + 1):
                if not has_H_wall[r][r + h][vc] and (col_sum[vc][r + h] - col_sum[vc][r]) == h:
                    return 1
                    
    if d_man > 8:
        return 3
        
    # Check distance 2
    # Intermediate cell 1: (tr, vc)
    if in_S[tr][vc]:
        c_min = min(tc, vc)
        d_h = abs(vc - tc)
        if not has_V_wall[tr][c_min][c_min + d_h]:
            w_h = 2 * d_h
            start_c = max(0, c_min - d_h + 1)
            end_c = min(c_min, N - w_h)
            h_ok = False
            for c in range(start_c, end_c + 1):
                if not has_V_wall[tr][c][c + w_h] and (row_sum[tr][c + w_h] - row_sum[tr][c]) == w_h:
                    h_ok = True
                    break
            if h_ok:
                r_min = min(tr, vr)
                d_v = abs(vr - tr)
                if not has_H_wall[r_min][r_min + d_v][vc]:
                    h_v = 2 * d_v
                    start_r = max(0, r_min - d_v + 1)
                    end_r = min(r_min, N - h_v)
                    v_ok = False
                    for r in range(start_r, end_r + 1):
                        if not has_H_wall[r][r + h_v][vc] and (col_sum[vc][r + h_v] - col_sum[vc][r]) == h_v:
                            v_ok = True
                            break
                    if v_ok:
                        return 2
                        
    # Intermediate cell 2: (vr, tc)
    if in_S[vr][tc]:
        r_min = min(tr, vr)
        d_v = abs(vr - tr)
        if not has_H_wall[r_min][r_min + d_v][tc]:
            h_v = 2 * d_v
            start_r = max(0, r_min - d_v + 1)
            end_r = min(r_min, N - h_v)
            v_ok = False
            for r in range(start_r, end_r + 1):
                if not has_H_wall[r][r + h_v][tc] and (col_sum[tc][r + h_v] - col_sum[tc][r]) == h_v:
                    v_ok = True
                    break
            if v_ok:
                c_min = min(tc, vc)
                d_h = abs(vc - tc)
                if not has_V_wall[vr][c_min][c_min + d_h]:
                    w_h = 2 * d_h
                    start_c = max(0, c_min - d_h + 1)
                    end_c = min(c_min, N - w_h)
                    h_ok = False
                    for c in range(start_c, end_c + 1):
                        if not has_V_wall[vr][c][c + w_h] and (row_sum[vr][c + w_h] - row_sum[vr][c]) == w_h:
                            h_ok = True
                            break
                    if h_ok:
                        return 2
                        
    return 3

def get_transitions(u, col_sum, row_sum, has_H_wall, has_V_wall, N):
    r_A, c_A = u
    transitions = []
    
    # 1. Vertical transitions: swap (r_A, c_A) with (r_B, c_A)
    for r_B in range(N):
        if r_B == r_A:
            continue
        r_min = min(r_A, r_B)
        d = abs(r_B - r_A)
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

def get_op_delta_cost(op_type, r, c, h, w, pos_to_card, N):
    delta_cost = 0
    if op_type == 'V':
        half_h = h // 2
        for x in range(half_h):
            r1 = r + x
            r2 = r1 + half_h
            for y in range(w):
                cy = c + y
                card1 = pos_to_card[r1][cy]
                card2 = pos_to_card[r2][cy]
                
                t1_r, t1_c = card1 // N, card1 % N
                t2_r, t2_c = card2 // N, card2 % N
                
                # Before dist
                d1_b = abs(r1 - t1_r) + abs(cy - t1_c)
                d2_b = abs(r2 - t2_r) + abs(cy - t2_c)
                
                # After dist
                d1_a = abs(r2 - t1_r) + abs(cy - t1_c)
                d2_a = abs(r1 - t2_r) + abs(cy - t2_c)
                
                delta_cost += (d1_a + d2_a) - (d1_b + d2_b)
    elif op_type == 'H':
        half_w = w // 2
        for x in range(h):
            rx = r + x
            for y in range(half_w):
                c1 = c + y
                c2 = c1 + half_w
                card1 = pos_to_card[rx][c1]
                card2 = pos_to_card[rx][c2]
                
                t1_r, t1_c = card1 // N, card1 % N
                t2_r, t2_c = card2 // N, card2 % N
                
                # Before dist
                d1_b = abs(rx - t1_r) + abs(c1 - t1_c)
                d2_b = abs(rx - t2_r) + abs(c2 - t2_c)
                
                # After dist
                d1_a = abs(rx - t1_r) + abs(c2 - t1_c)
                d2_a = abs(rx - t2_r) + abs(c1 - t2_c)
                
                delta_cost += (d1_a + d2_a) - (d1_b + d2_b)
    return delta_cost

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

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    
    # Read initial card placement
    a = []
    idx = 1
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        a.append(row)
        
    # Read vertical walls: N strings of length N-1
    V = []
    for r in range(N):
        V.append(input_data[idx])
        idx += 1
        
    # Read horizontal walls: N-1 strings of length N
    H = []
    for r in range(N-1):
        H.append(input_data[idx])
        idx += 1
        
    # Precompute walls check table for fast transitions checks
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
                
    # Build grid graph adjacency list (only for connectivity check)
    adj = [[[] for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            # Check right neighbor: (r, c+1)
            if c + 1 < N:
                if V[r][c] == '0':
                    adj[r][c].append((r, c+1))
                    adj[r][c+1].append((r, c))
            # Check down neighbor: (r+1, c)
            if r + 1 < N:
                if H[r][c] == '0':
                    adj[r][c].append((r+1, c))
                    adj[r+1][c].append((r, c))
                    
    # Initialize card tracking
    card_to_pos = [None] * (N * N)
    pos_to_card = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            val = a[r][c]
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
    
    while len(S) > 1:
        # Build G[S] adjacency list (for Tarjan)
        adj_in_S = {}
        for node in S:
            adj_in_S[node] = [neighbor for neighbor in adj[node[0]][node[1]] if in_S[neighbor[0]][neighbor[1]]]
            
        # Find cut vertices in G[S] using Tarjan's algorithm
        root = next(iter(S))
        dfn = {}
        low = {}
        is_cut = set()
        timer = 0
        children_count = 0
        
        def dfs(u, p=(-1, -1)):
            nonlocal timer, children_count
            timer += 1
            dfn[u] = low[u] = timer
            for v in adj_in_S[u]:
                if v == p:
                    continue
                if v in dfn:
                    low[u] = min(low[u], dfn[v])
                else:
                    if u == root:
                        children_count += 1
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if u != root and low[v] >= dfn[u]:
                        is_cut.add(u)
                        
        dfs(root)
        if children_count > 1:
            is_cut.add(root)
            
        candidates = [node for node in S if node not in is_cut]
        if not candidates:
            candidates = list(S)
            
        # 1. Estimate transition distance for all candidates
        best_v = None
        ops_in_path = None
        
        # Group candidates by estimated distance
        dist_groups = {0: [], 1: [], 2: [], 3: []}
        for v in candidates:
            target_card = v[0] * N + v[1]
            target_pos = card_to_pos[target_card]
            d_est = estimate_transition_dist(v, target_pos, col_sum, row_sum, has_H_wall, has_V_wall, in_S, N)
            dist_groups[d_est].append(v)
            
        if dist_groups[0]:
            dist_groups[0].sort(key=lambda x: (len(adj_in_S[x]), x))
            best_v = dist_groups[0][0]
            ops_in_path = []
        elif dist_groups[1]:
            # Sort by neighbor count, evaluate top 10
            dist_groups[1].sort(key=lambda x: (len(adj_in_S[x]), x))
            candidates_1_to_eval = dist_groups[1][:10]
            
            candidates_1_evaluated = []
            for v in candidates_1_to_eval:
                target_pos = card_to_pos[v[0] * N + v[1]]
                transitions = get_transitions(target_pos, col_sum, row_sum, has_H_wall, has_V_wall, N)
                op = None
                for nxt, o in transitions:
                    if nxt == v:
                        op = o
                        break
                if op is not None:
                    op_type, r, c, h, w = op
                    if op_type == 'V':
                        r_exp, c_exp, h_exp, w_exp = expand_vertical_op(r, c, h, col_sum, V, H, N)
                    else:
                        r_exp, c_exp, h_exp, w_exp = expand_horizontal_op(r, c, w, row_sum, V, H, N)
                    cost = get_op_delta_cost(op_type, r_exp, c_exp, h_exp, w_exp, pos_to_card, N)
                    candidates_1_evaluated.append((cost, len(adj_in_S[v]), v, (op_type, r_exp, c_exp, h_exp, w_exp)))
            
            if candidates_1_evaluated:
                candidates_1_evaluated.sort(key=lambda x: (x[0], x[1], x[2]))
                _, _, best_v, expanded_op = candidates_1_evaluated[0]
                ops_in_path = [expanded_op]
            else:
                best_v = dist_groups[1][0]
        elif dist_groups[2]:
            # Sort by neighbor count, evaluate top 5
            dist_groups[2].sort(key=lambda x: (len(adj_in_S[x]), x))
            candidates_2_to_eval = dist_groups[2][:5]
            
            candidates_2_evaluated = []
            for v in candidates_2_to_eval:
                target_pos = card_to_pos[v[0] * N + v[1]]
                q = deque([v])
                vis = {v: None}
                op_vis = {}
                found = False
                while q and not found:
                    curr = q.popleft()
                    transitions = get_transitions(curr, col_sum, row_sum, has_H_wall, has_V_wall, N)
                    for nxt, op in transitions:
                        if nxt not in vis:
                            vis[nxt] = curr
                            op_vis[nxt] = op
                            q.append(nxt)
                            if nxt == target_pos:
                                found = True
                                break
                if found:
                    curr = target_pos
                    ops_list = []
                    while curr is not None:
                        parent = vis[curr]
                        if parent is not None:
                            ops_list.append(op_vis[curr])
                        curr = parent
                    
                    op = ops_list[0]
                    op_type, r, c, h, w = op
                    if op_type == 'V':
                        r_exp, c_exp, h_exp, w_exp = expand_vertical_op(r, c, h, col_sum, V, H, N)
                    else:
                        r_exp, c_exp, h_exp, w_exp = expand_horizontal_op(r, c, w, row_sum, V, H, N)
                    cost = get_op_delta_cost(op_type, r_exp, c_exp, h_exp, w_exp, pos_to_card, N)
                    candidates_2_evaluated.append((cost, len(adj_in_S[v]), v, ops_list))
            
            if candidates_2_evaluated:
                candidates_2_evaluated.sort(key=lambda x: (x[0], x[1], x[2]))
                _, _, best_v, ops_list = candidates_2_evaluated[0]
                ops_in_path = ops_list
            else:
                best_v = dist_groups[2][0]
        else:
            candidates_3 = dist_groups[3]
            queues = {v: deque([v]) for v in candidates_3}
            visited_grid = {v: {v} for v in candidates_3}
            targets = {v: card_to_pos[v[0] * N + v[1]] for v in candidates_3}
            
            found_candidates = []
            while not found_candidates:
                for v in candidates_3:
                    q = queues[v]
                    vis = visited_grid[v]
                    tgt = targets[v]
                    
                    level_sz = len(q)
                    if level_sz == 0:
                        continue
                        
                    found = False
                    for _ in range(level_sz):
                        curr = q.popleft()
                        for nxt in adj_in_S[curr]:
                            if nxt not in vis:
                                vis.add(nxt)
                                q.append(nxt)
                                if nxt == tgt:
                                    found = True
                    if found:
                        found_candidates.append(v)
            found_candidates.sort(key=lambda x: (len(adj_in_S[x]), x))
            best_v = found_candidates[0]
            
        # 2. Run transition-graph BFS only for this best_v (if not already found)
        target_pos = card_to_pos[best_v[0] * N + best_v[1]]
        if target_pos == best_v:
            ops_in_path = []
        elif ops_in_path is None:
            q = deque([best_v])
            vis = {best_v: None}
            op_vis = {}
            found = False
            while q and not found:
                curr = q.popleft()
                transitions = get_transitions(curr, col_sum, row_sum, has_H_wall, has_V_wall, N)
                for nxt, op in transitions:
                    if nxt not in vis:
                        vis[nxt] = curr
                        op_vis[nxt] = op
                        q.append(nxt)
                        if nxt == target_pos:
                            found = True
                            break
            # Reconstruct operations
            ops_in_path = []
            curr = target_pos
            while curr is not None:
                parent = vis[curr]
                if parent is not None:
                    ops_in_path.append(op_vis[curr])
                curr = parent
                
        # Expand and apply operations
        for op in ops_in_path:
            op_type, r, c, h, w = op
            # If the operation was already expanded (e.g. from evaluations), its width/height might be > 1.
            # But the BFS returns default ops with width/height = 1.
            # We check if it is already expanded (if we evaluated it, we stored the expanded op).
            # Wait, `ops_list` stores default ops, but `candidates_1_evaluated` stores expanded ops.
            # To be safe, we always re-run expansion on the default op, or if it's already expanded, expansion will just return it.
            # Let's see: expand_vertical_op takes `h`, which is the height. If the input is V, it expands width.
            # Since h is the height (which is invariant under expansion), expand_vertical_op will correctly expand it.
            # For H, w is the width (invariant under expansion), so expand_horizontal_op will correctly expand it.
            # So re-running expansion is always correct and safe!
            if op_type == 'V':
                r_exp, c_exp, h_exp, w_exp = expand_vertical_op(r, c, h, col_sum, V, H, N)
            else:
                r_exp, c_exp, h_exp, w_exp = expand_horizontal_op(r, c, w, row_sum, V, H, N)
                
            ops.append(f"{op_type} {r_exp} {c_exp} {h_exp} {w_exp}")
            apply_op(op_type, r_exp, c_exp, h_exp, w_exp, pos_to_card, card_to_pos)
            
        S.remove(best_v)
        in_S[best_v[0]][best_v[1]] = False
        # Update col_sum and row_sum
        br, bc = best_v
        for r in range(br + 1, N + 1):
            col_sum[bc][r] -= 1
        for c in range(bc + 1, N + 1):
            row_sum[br][c] -= 1
        
    for op in ops:
        print(op)

if __name__ == '__main__':
    solve()
