import bisect
from itertools import accumulate
n,l,r = map(int,input().split())
a = list(map(int,input().split()))

acc_a = [0] + list(accumulate(a))
# print(acc_a)

b = [0]
ans = 0
for i in range(1,n+1):
    left = bisect.bisect_left(b,acc_a[i]-r)
    right = bisect.bisect_right(b,acc_a[i]-l)
    # print(acc_a[i]-r,acc_a[i]-l)
    # print(right - left)
    ans += right - left
    # print(b)
    bisect.insort(b,acc_a[i])
print(ans)