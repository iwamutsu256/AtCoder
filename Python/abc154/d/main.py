from itertools import accumulate

n,k = map(int,input().split())
p = list(map(int,input().split()))

q = [p[i]+1 for i in range(len(p))]

q_acc = [0]+list(accumulate(q))
ans = 0
for i in range(n-k+1):
    kitai = q_acc[i+k] - q_acc[i]
    ans = max(ans, kitai)
print(ans/2)