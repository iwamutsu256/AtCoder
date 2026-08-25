n,q = map(int,input().split())
p = list(map(int,input().split()))
pq = [[0 for _ in range(n+1)] for _ in range(2)]

for i in range(1,len(p)+1):
    pq[0][i] = p[i-1]
    pq[1][p[i-1]] = i

pi = 0

for _ in range(q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        px, py = pq[pi][query[1]], pq[pi][query[2]]
        pq[pi][query[1]],pq[pi][query[2]] = pq[pi][query[2]],pq[pi][query[1]]
        pq[pi^1][px],pq[pi^1][py] = pq[pi^1][py],pq[pi^1][px]
    else:
        pi ^= 1

print(*pq[pi][1:])