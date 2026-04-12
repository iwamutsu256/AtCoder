#関数
def root(x):
    while True:
        if par[x] == -1:
            break
        else:
            x = par[x]
    return x
#rootまでの辺の数
def length(x):
    count = 1
    while True:
        if par[x] == -1:
            break
        else:
            x = par[x]
            count += 1
    return count

def level(x):
    Rootx = root(x)
    return lev[Rootx]

def rootlength(x):
    return length(x)+level(x)

def unite(u,v):
    Rootu = root(u)
    Rootv = root(v)
    if Rootu == Rootv:
        return
    if A[u] < A[v]:
        if length(u)+rootlength(v) <= H:
            par[v] = u
            size[Rootu] = size[Rootv]+size[Rootu]
            lev[Rootu] = max(lev[Rootu],length(u)+rootlength(v))
        elif length(v)+rootlength(u) <= H:
            par[u] = v
            size[Rootv] = size[Rootv]+size[Rootu]
            lev[Rootv] = max(lev[Rootv],length(v)+rootlength(u))
    else:
        if length(v)+rootlength(u) <= H:
            par[u] = v
            size[Rootv] = size[Rootv]+size[Rootu]
            lev[Rootv] = max(lev[Rootv],length(v)+rootlength(u))
        elif length(u)+rootlength(v) <= H:
            par[v] = u
            size[Rootu] = size[Rootv]+size[Rootu]
            lev[Rootu] = max(lev[Rootu],length(u)+rootlength(v))
    return



#入力
N,M,H = map(int,input().split())
A = [int(x) for x in input().split()]
graph = [[] for _ in range(N)]
for _ in range(M):
    u,v = map(int,input().split())
    graph[u].append(v)
    graph[v].append(u)
point = [[] for _ in range(N)]
for i in range(N):
    x,y = map(int,input().split())
    point[i].append(x)
    point[i].append(y)


par = [-1]*N
size = [1]*N
lev = [1]*N


#計算
for k in range(10,100,5):
    for i in range(N):
        for j in range(len(graph[i])):
            if abs(A[i]-A[graph[i][j]])<k:
                unite(i,graph[i][j])
    for l in range(N):
        print(par[l],end=" ")
    print()

#for l in range(N):
#    print(par[i],end=" ")
#print()