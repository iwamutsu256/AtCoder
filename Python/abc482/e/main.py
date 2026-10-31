import sys
from collections import deque, Counter
sys.setrecursionlimit(10**6)

n = int(input())
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)

c = [0] + list(map(int, input().split()))

def get_dist(s):
    dist = [-1] * (n + 1)
    parent = [-1] * (n + 1)
    queue = deque([s])
    dist[s] = 0
    while queue:
        v = queue.popleft()
        for v2 in g[v]:
            if dist[v2] == -1:
                dist[v2] = dist[v] + 1
                parent[v2] = v
                queue.append(v2)
    return dist, parent

# 直径の端点 u, v を求める
dist_1, _ = get_dist(1)
u = dist_1.index(max(dist_1[1:]))

dist_u, parent_u = get_dist(u)
v = dist_u.index(max(dist_u[1:]))
D = dist_u[v]

# u から v へのパスを取得
path = []
curr = v
while curr != -1:
    path.append(curr)
    curr = parent_u[curr]

ans = 0

if D % 2 == 0:
    # 直径が偶数：中心頂点は1つ
    center = path[D // 2]
    target_d = D // 2
    
    # 中心からの距離を取得
    dist_c, _ = get_dist(center)
    
    # 全体の target_d 距離にある頂点の色カウント
    total_counts = Counter()
    for i in range(1, n + 1):
        if dist_c[i] == target_d:
            total_counts[c[i]] += 1
            
    # 全体での同じ色のペア数
    for count in total_counts.values():
        ans += count * (count - 1) // 2
        
    # 各部分木内での重複ペアを引く
    for sub in g[center]:
        # center を通らずに sub から探索
        q = deque([sub])
        visited = {center, sub}
        sub_counts = Counter()
        
        while q:
            curr = q.popleft()
            if dist_c[curr] == target_d:
                sub_counts[c[curr]] += 1
            for nxt in g[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
                    
        for count in sub_counts.values():
            ans -= count * (count - 1) // 2

else:
    # 直径が奇数：中心辺は (c1, c2)
    c1 = path[D // 2]
    c2 = path[D // 2 + 1]
    target_d = (D - 1) // 2
    
    # c1 側の連結成分の探索
    q1 = deque([c1])
    visited1 = {c1, c2}
    dist1 = {c1: 0}
    counts1 = Counter()
    
    while q1:
        curr = q1.popleft()
        if dist1[curr] == target_d:
            counts1[c[curr]] += 1
        for nxt in g[curr]:
            if nxt not in visited1:
                visited1.add(nxt)
                dist1[nxt] = dist1[curr] + 1
                q1.append(nxt)
                
    # c2 側の連結成分の探索
    q2 = deque([c2])
    visited2 = {c1, c2}
    dist2 = {c2: 0}
    counts2 = Counter()
    
    while q2:
        curr = q2.popleft()
        if dist2[curr] == target_d:
            counts2[c[curr]] += 1
        for nxt in g[curr]:
            if nxt not in visited2:
                visited2.add(nxt)
                dist2[nxt] = dist2[curr] + 1
                q2.append(nxt)
                
    for col, count in counts1.items():
        ans += count * counts2[col]

print(ans)