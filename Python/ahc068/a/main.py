import sys
from collections import deque

# Increase recursion limit just in case
sys.setrecursionlimit(2000)

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
        
    # Build grid graph adjacency list
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
    ops = []
    
    while len(S) > 1:
        # Build G[S] adjacency list
        adj_in_S = {}
        for node in S:
            adj_in_S[node] = [neighbor for neighbor in adj[node[0]][node[1]] if neighbor in S]
            
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
        
        # If no candidates are found (should not happen on connected S), safety fallback
        if not candidates:
            candidates = list(S)
            
        # Level-by-level BFS from all candidates v to their targets in G[S]
        best_v = None
        path = None
        
        # Check distance 0 first
        for v in candidates:
            target_card = v[0] * N + v[1]
            target_pos = card_to_pos[target_card]
            if target_pos == v:
                best_v = v
                path = [v]
                break
                
        if best_v is None:
            queues = {}
            visited = {}
            targets = {}
            for v in candidates:
                target_card = v[0] * N + v[1]
                target_pos = card_to_pos[target_card]
                queues[v] = deque([v])
                visited[v] = {v: None}
                targets[v] = target_pos
                
            found_candidates = []
            while not found_candidates:
                for v in candidates:
                    q = queues[v]
                    vis = visited[v]
                    tgt = targets[v]
                    
                    level_sz = len(q)
                    if level_sz == 0:
                        continue
                        
                    found = False
                    for _ in range(level_sz):
                        curr = q.popleft()
                        for nxt in adj_in_S[curr]:
                            if nxt not in vis:
                                vis[nxt] = curr
                                q.append(nxt)
                                if nxt == tgt:
                                    found = True
                    if found:
                        found_candidates.append(v)
                        
            # Select the first candidate that found its target
            best_v = found_candidates[0]
            # Reconstruct path
            path = []
            curr = targets[best_v]
            while curr is not None:
                path.append(curr)
                curr = visited[best_v][curr]
                
        # Perform swaps along path (from target_pos to best_v)
        for i in range(len(path) - 1):
            p_curr = path[i]
            p_next = path[i+1]
            
            r_curr, c_curr = p_curr
            r_next, c_next = p_next
            
            if r_curr == r_next:
                c_min = min(c_curr, c_next)
                ops.append(f"H {r_curr} {c_min} 1 2")
            else:
                r_min = min(r_curr, r_next)
                ops.append(f"V {r_min} {c_curr} 2 1")
                
            # Swap cards
            card_curr = pos_to_card[r_curr][c_curr]
            card_next = pos_to_card[r_next][c_next]
            
            pos_to_card[r_curr][c_curr] = card_next
            pos_to_card[r_next][c_next] = card_curr
            
            card_to_pos[card_curr] = p_next
            card_to_pos[card_next] = p_curr
            
        S.remove(best_v)
        
    # Output all operations
    for op in ops:
        print(op)

if __name__ == '__main__':
    solve()
