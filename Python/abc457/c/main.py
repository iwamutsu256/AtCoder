N,K = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(N)]
C = list(map(int,input().split()))
K -= 1
for i in range(N):
    if C[i]*A[i][0] <= K:
        K -= C[i]*A[i][0]
    else:
        print(A[i][K%A[i][0]+1])
        break