from collections import defaultdict, deque

n,m = map(int,input().split())
road = defaultdict(list)
for i in range(m):
    u,v,c = map(int,input().split())
    road[u].append((v,c,i))

start = 1

queue = deque()
queue.append((start, 0, -1))

visited = [False for _ in range(m)]

while queue:
    city, dist, color =queue.popleft()
    if city == n:
        print(dist)
        break
    for v,c,i in road[city]:
        if color != c and not visited[i]:
            queue.append((v,dist+1,c))
            visited[i] = True
else:
    print(-1)

