N,T,P = map(int,input().split())
L = list(map(int,input().split()))
L.sort(reverse=True)
length = L[P-1]
if T <= length:
    print(0)
else:
    print(T-length)
