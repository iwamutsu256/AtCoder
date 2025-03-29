N,M = map(int,input().split())
mp = [[] for _ in range(N+1)]
seen = [False] * (N)
for i in range(M):
    u,v = map(int,input().split())
    mp[u].append(v)
    mp[v].append(u)


def dfs(start):
    stack = [start]
    seen[start-1] = True

    while stack:
        v = stack.pop()
        for next_v in mp[v]:
            if not seen[next_v-1]:
                seen[next_v-1] = True
                stack.append(next_v)
ans = M-N
for i in range(N):
    if not seen[i]:
        ans += 1
        dfs(i+1)
print(ans)