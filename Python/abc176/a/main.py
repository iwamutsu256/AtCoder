N,X,T = map(int,input().split())
if N % X == 0:
    print(N*T//X)
else:
    print(T*(N//X + 1))