H,W,N = map(int,input().split())
X = {i+1:set() for i in range(H)}
Y = {i+1:set() for i in range(W)}
for i in range(N):
    X1,Y1 = map(int,input().split())
    X[X1].add(Y1)
    Y[Y1].add(X1)
#print(X,Y)

Q = int(input())
for i in range(Q):
    S,T = map(int,input().split())
    if S == 1:
        print(len(X[T]))
        for j in X[T]:
            Y[j].remove(T)
        X[T] = set()
    else:
        print(len(Y[T]))
        for j in Y[T]:
            X[j].remove(T)
        Y[T] = set()