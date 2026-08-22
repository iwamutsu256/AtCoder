import sys
sys.setrecursionlimit(10**6)

def dfs(pos, parent, dist):
    state[pos] = 1
    path.append(pos)
    for next_pos in node[pos]:
        if next_pos == pos:
            continue
        if state[next_pos] == 0:
            parent[next_pos] = pos
            dist[next_pos] = dist+1
            dfs(next_pos,pos,dist+1)
        elif state[next_pos] == 1 and (dist-dist[next_pos])%2 == 0:
            current = pos
            path.append(next_pos+1)
            while current != next_pos:
                path.append(current+1)
                current = parent[current]
            # path.append(next_pos)
            return path
    state[pos] = 2
    return -1

t = int(input())
for _ in range(t):
    n,m = map(int,input().split())
    node = [[] for _ in range(n)]
    for i in range(m):
        a,b = map(int,input().split())
        a -= 1
        b -= 1
        node[a].append(b)
        node[b].append(a)

    path = []
    parent = [-1]*n
    state = [0]*n
    dist = [-1]*n
    p = dfs(0,0,0)
    if p == -1:
        print(-1)
    else:
        print(*p)