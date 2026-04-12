N,M = map(int,input().split())
if N == 1:
    print(N*(M+1))
else:
    X = (N**(M+1)-1)//(N-1)
    if X > 1000000000:
        print("inf")
    else:
        print(X)