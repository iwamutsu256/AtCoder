from itertools import accumulate
import bisect

n,m,k = map(int,input().split())
x,y = map(int,input().split())

a = list(map(int,input().split()))
b = list(map(int,input().split()))

a = sorted(a)
b = sorted(b)

acc_a = list(accumulate(a))

# print(acc_a)

now_k = 0
otsuri = 0

kind = 0

for i in range(m+1):
    if i != 0:
        now_k += -(-b[i-1]//k)
        otsuri += (-(-b[i-1]//k))*k - b[i-1]
    if now_k > y:
        break
    # print(f"お釣り:{otsuri}")
    now_money = (y-now_k)*k + x + otsuri
    a_cnt = bisect.bisect_right(acc_a,now_money)
    # print(now_money, a_cnt)
    kind = max(kind,i+a_cnt)
print(kind)