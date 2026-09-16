import sys
n,m = map(int,input().split())
if m == 0:
    print(1)
    sys.exit()
a = list(map(int,input().split()))

a = sorted(a)
b = []
s = 0
for i in range(m):
    # print(a[i] - s - 1)
    if a[i] - s - 1 > 0:
        b.append(a[i]-s-1)
    s = a[i]
if n - s > 0:
    b.append(n-s)

# print(b)
if b == []:
    small = 0
else:
    small = min(b)

ans = 0
for i in range(len(b)):
    if b[i] % small == 0:
        ans += b[i]//small
    else:
        ans += b[i]//small + 1
print(ans)