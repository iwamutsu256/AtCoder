n,m = map(int,input().split())
a = list(map(int,input().split()))
b = list(map(int,input().split()))
# 先頭奇数か
ki = 0
gu = 0
aki = a.copy()
agu = a.copy()
for i in range(1,n):
    l = a[i-1]
    r = a[i]
    c = b[i-1]
    if i == 1:
        if l % 2 == 0:
            ki += 1
            aki[0] += 1
        else:
            gu += 1
            agu[0] += 1
    # print(aki[i]+aki[i-1])
    if c % 2 != (aki[i]+aki[i-1])%2:
        ki += 1
        aki[i] += 1
    # print(agu[i]+agu[i-1])
    if c % 2 != (agu[i] + agu[i-1])%2:
        gu += 1
        agu[i] += 1
    # print(i,aki,agu)
print(min(ki,gu))