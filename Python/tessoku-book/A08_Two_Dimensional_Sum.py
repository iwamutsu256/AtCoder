H,W = map(int,input().split())
X = [[int(x) for x in input().split()] for _ in range(H)]
Q = int(input())
Y = [[int(0) for _ in range(W+1)] for _ in range(H+1)]
#print(Y)
#print(X)
#横向きの累積和
for i in range(1,H+1):
    for j in range(1,W+1):
        Y[i][j] = Y[i][j-1]+X[i-1][j-1]
#print(Y)
#縦向きの累積和
for i in range(1,H+1):
    for j in range(1,W+1):
        Y[i][j] = Y[i-1][j]+Y[i][j]
#print(Y)
for i in range(Q):
    A,B,C,D = map(int,input().split())
    print(Y[C][D]+Y[A-1][B-1]-Y[A-1][D]-Y[C][B-1])