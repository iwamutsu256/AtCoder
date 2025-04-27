N,M,Q = map(int,input().split())
X = [set() for _ in range(N)]
is_all = [False for _ in range(N)]
for i in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        X[query[1]-1].add(query[2])
    elif query[0] == 2:
        is_all[query[1]-1] = True
    else:
        if is_all[query[1]-1] or (query[2] in X[query[1]-1]):
            print("Yes")
        else:
            print("No")

