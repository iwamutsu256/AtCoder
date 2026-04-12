N,K = map(int,input().split())
A = list(map(int,input().split()))
ans = 1
for i in range(len(A)):
    if ans * A[i] >= 10**K:
        ans = 1
    else:
        ans = ans * A[i]
print(ans)