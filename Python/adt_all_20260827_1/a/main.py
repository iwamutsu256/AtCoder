n,p,q,r,s = map(int,input().split())
a = [0] + list(map(int,input().split()))
b = [0 for _ in range(n+1)]
for i in range(n+1):
    if p <= i <= q:
        b[i] = a[r+(i-p)]
    elif r<= i <= s:
        b[i] = a[p+(i-r)]
    else:
        b[i] = a[i]
print(*b[1:])