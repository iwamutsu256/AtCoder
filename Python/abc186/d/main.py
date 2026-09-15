from itertools import accumulate

n = int(input())
a = list(map(int,input().split()))
a = sorted(a)

a_sum = list(accumulate(a))
ans = 0
for i in range(1,n):
    ans += a[i]*i - a_sum[i-1]
print(ans)