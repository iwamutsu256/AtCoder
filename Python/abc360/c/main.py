N = int(input())
A = list(map(int,input().split()))
W = list(map(int,input().split()))
H = [[] for _ in range(N)]
for i in range(N):
    H[A[i]-1].append(W[i])
count = 0
for i in range(N):
    if len(H[i]) > 1:
        H[i].sort()
        for j in range(len(H[i])-1):
            count += H[i][j]
print(count)