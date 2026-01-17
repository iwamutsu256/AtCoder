def dfs(cur,count,cost):
    if count == L:
        if S <= cost <= T:
            Ans.add(cur)
        return
    for i in range(len(Points[cur])):
        dfs(Points[cur][i][0],count + 1,cost + Points[cur][i][1])

N,M,L,S,T = map(int,input().split())
Points = [[] for _ in range(N+1)]
for _ in range(M):
    U,V,C = map(int,input().split())
    Points[U].append((V,C))
Ans = set()
dfs(1,0,0)
answer = list(Ans)
print(" ".join(map(str,sorted(answer))))