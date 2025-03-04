N = int(input())
A = list(map(int,input().split()))
ans = 1000000000
T = [-1 for _ in range(1000001)]
for i in range(N):
    if T[A[i]] == -1:
        T[A[i]] = i
    else:
        ans = min(ans,i-T[A[i]])
        T[A[i]] = i
if ans > 10000000:
    print(-1)
else:
    print(ans+1)
