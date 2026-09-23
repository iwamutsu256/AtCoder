from collections import deque, defaultdict

n,m = map(int,input().split())

edges = defaultdict(list)
for _ in range(m):
    a,b = map(int,input().split())
    edges[a].append(b)
    edges[b].append(a)

visited = [False for _ in range(n+1)]
pointer = [-1 for _ in range(n+1)]

pointer[1] = 1
current = 1

queue = deque([])

queue.append(1)
visited[1] = True

while queue:
    current = queue.popleft()
    for node in edges[current]:
        if visited[node] == False:
            visited[node] = True
            pointer[node] = current
            queue.append(node)

print("Yes")

for i in range(n-1):
    print(pointer[i+2])