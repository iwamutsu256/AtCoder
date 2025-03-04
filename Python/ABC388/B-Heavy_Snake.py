N,D = map(int,input().split())
T = [0]*N
L = [0]*N
for i in range(N):
    T[i], L[i] = map(int,input().split())
for i in range(1,D+1):
    ans = 0
    for j in range(N):
        ans = max(ans,T[j]*(L[j]+i))
    print(ans)
