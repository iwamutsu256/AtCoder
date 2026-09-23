from itertools import combinations

n = int(input())
a = list(map(int,input().split()))


ans = 2**30 + 1
# いくつのグループに分割するか
for i in range(1,n+1):
    for index in combinations([int(x) for x in range(1,n)],i-1):
        # print(index)
        now = 0
        xor = 0
        for j in index:
            ro = 0
            for k in range(now, j):
                ro |= a[k]
                # print(a[k],end="")
            # print("|",end="")
            xor ^= ro
            now = j
        ro = 0
        for k in range(now, n):
            ro |= a[k]
            # print(a[k],end="")
        # print("|",end="")
        xor ^= ro
        ans = min(xor, ans)
print(ans)
