def rotate(n):
    right = []
    for i in range(N):
        right.append((i+n-1) % N + 1)
    return right
def arcrot(n):
    left = []
    for i in range(N):
        left.append((-i+n-1)%N+1)
    return left

N, Q = map(int,input().split())
r = 2
l = 1
sum = 0
for i in range(Q):
    H,T = input().split()
    T = int(T)
    if H == "R":
        R = rotate(r)
        L = arcrot(r)
        if R.index(l) > R.index(T):
            sum += R.index(T)
        else:
            sum += L.index(T)
        r = T
    else:
        R = rotate(l)
        L = arcrot(l)
        if R.index(r) > R.index(T):
            sum += R.index(T)
        else:
            sum += L.index(T)
        l = T
print(sum)