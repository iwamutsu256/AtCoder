#累積和
N,Q = map(int,input().split())
A = [int(x) for x in input().split()]
#累積和を記録する配列
B = [0]
for i in range(N):
    B.append(B[-1] + A[i])
#print(B)
for i in range(Q):
    L,R = map(int,input().split())
    print(B[R]-B[L-1])
