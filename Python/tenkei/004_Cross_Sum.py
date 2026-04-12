H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
gyou = []
retsu = []
for i in range(H):
    gyou.append(sum(A[i]))
for i in range(W):
    count = 0
    for j in range(H):
        count += A[j][i]
    retsu.append(count)
for i in range(H):
    for j in range(W):
        print(gyou[i]+retsu[j]-A[i][j],end=" ")
    print()
