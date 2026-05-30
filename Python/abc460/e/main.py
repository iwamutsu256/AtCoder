def concat(a,b):
    a = str(a)
    b = str(b)
    return(int(a+b))

T = int(input())
for _ in range(T):
    N,M = map(int,input().split())
