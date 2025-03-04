N,M = map(int,input().split())
S = set()
count = 0
for i in range(M):
    u,v = map(int,input().split())
    if u == v:
        count += 1
    elif {u,v} in S:
        count += 1
    else:
        S.add(frozenset({u,v}))
print(count)
