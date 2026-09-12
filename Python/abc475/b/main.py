import math
n = int(input())
a = list(map(int,input().split()))
ans = [0, 0, 0]
for i in range(n):
    m = a[i] // 1000
    if a[i] % 1000 != 0:
        m += 1
    pay = m * 1000
    back = pay - a[i]
    back = list(str(back).zfill(3))
    for i in range(3):
        ans[2-i] += int(back[i])

print(*ans)