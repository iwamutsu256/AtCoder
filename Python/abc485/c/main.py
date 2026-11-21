n = int(input())
c = list(map(int,input().split()))

INF = 10**7

dist = [INF for _ in range(n)]

for i in range(1,n):
    if c[i] != c[i-1]:
        dist[i] = min(1,dist[i])
    else:
        dist[i] = min(dist[i-1] + 1,dist[i])

for i in range(n-2,-1,-1):
    if c[i] != c[i+1]:
        dist[i] = min(1,dist[i])
    else:
        dist[i] = min(dist[i+1]+1, dist[i])

print(*dist)