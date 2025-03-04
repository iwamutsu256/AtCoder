H,W,N = map(int,input().split())
G = [[0 for _ in range(W+2)] for _ in range(H+2)]
answer = [[0 for _ in range(W+2)] for _ in range(H+2)]
for i in range(N):
    A,B,C,D = map(int,input().split())
    G[A][B] += 1
    G[C+1][D+1] += 1
    G[A][D+1] -= 1
    G[C+1][B] -= 1
#横方向累積和
for i in range(1,H+1):
    for j in range(1,W+1):
        answer[i][j] = answer[i][j-1]+G[i][j]
#縦方向累積和
#forの添え字とrangeの幅に注意
for j in range(1,W+1):
    for i in range(1,H+1):
        answer[i][j] = answer[i-1][j] + answer[i][j]
#出力
for i in range(1,H+1):
    for j in range(1,W+1):
        print(answer[i][j],end=" ")
    print()
#print(answer)