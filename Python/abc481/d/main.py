from collections import defaultdict
import heapq, sys

n,m,s,t = map(int,input().split())

start = s
goal = t


path = defaultdict(list)
mins = defaultdict(lambda: 10**9)

for _ in range(m):
    a,b = map(int,input().split())
    path[a].append(b)
    mins[a] = min(mins[a],b)

# print(mins)

queue = []
cost = 0
heapq.heappush(queue,(cost,start))
visited = [False for _ in range(n+1)]
# visited[start] = True
while queue:
    cost, node = heapq.heappop(queue)
    if node == goal:
        break
    if visited[node]:
        continue
    visited[node] = True
    for next in path[node]:
        if visited[next]:
            continue
        if next == mins[node]:
            heapq.heappush(queue,(cost,next))
        else:
            heapq.heappush(queue,(cost+1,next))
else:
    print(-1)
    sys.exit()

print(cost)