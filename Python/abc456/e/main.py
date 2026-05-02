def dfs(city,day):
    seen[city][day%W] = True
    if S[city][(day+1)%W] == "o":
        if visited[city][(day+1)%W]:
            pass
        if seen[city][(day+1)%W] and not visited[city][(day+1)%W]:
            return True
        if dfs(city,day+1):
            return True
    for v in from_to[city]:
        if S[v][(day+1)%W] == "o":
            if visited[city][(day+1)%W]:
                pass
            if seen[city][(day+1)%W] and not visited[city][(day+1)%W]:
                return True
            if dfs(city,day+1):
                return True
    visited[city][day%W] = True
    return False
    

T = int(input())
for _ in range(T):
    N,M = map(int,input().split())
    from_to = [[] for _ in range(N+1)]
    for _ in range(M):
        U,V = map(int,input().split())
        from_to[U].append(V)
        from_to[V].append(U)
    W = int(input())
    S = [None]+[input() for _ in range(N)]
    seen = [[False for _ in range(W)] for _ in range(N+1)]
    visited = [[False for _ in range(W)] for _ in range(N+1)]
    # DFS
    # 現在何日目を保持
    queue = []
    ans = False
    for i in range(1,N+1):
        if S[i][0] == "o":
            if dfs(i,0):
                ans = True
    if ans:
        print("Yes")
    else:
        print("No")