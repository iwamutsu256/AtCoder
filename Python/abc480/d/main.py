from itertools import accumulate
import bisect
n,q = map(int,input().split())
a = list(map(int,input().split()))

nums = [int(x) for x in range(n+2)]
n_acc = list(accumulate(nums))
# print(n_acc)
a_acc = [0] + list(accumulate(a))
# print(a_acc)
b_acc = list(accumulate(a_acc))
# print(b_acc)

def query(n):
    dan = bisect.bisect_left(n_acc,n)
    if n_acc[dan] - n == 0:
        return b_acc[dan]
    else:
        return a_acc[n-n_acc[dan-1]]+b_acc[dan-1]

for _ in range(q):
    l,r = map(int,input().split())
    print(query(r)-query(l-1))