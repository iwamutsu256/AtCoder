N,K = map(int,input().split())
A = [0]*(10**6+1)
for i in range(K):
    A[i] = 1
for i in range(K,N+1):
    if i == K:
        A[i] = K
    else:
        A[i] = (2*A[i-1] - A[i - 1 - K])% 1000000000
print(A[N])