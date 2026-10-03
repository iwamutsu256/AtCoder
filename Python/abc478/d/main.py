from itertools import accumulate
import heapq

n,q = map(int,input().split())
querys = []
heapq.heapify(querys)
for _ in range(q):
    l,r,x = map(int,input().split())
    heapq.heappush(querys,[l,x,1])
    heapq.heappush(querys,[r+1,x,-1])

# print(querys)

counter = [0 for _ in range(q)]
s = [0 for _ in range(n+2)]
for _ in range(len(querys)):
    t,x,sgn = heapq.heappop(querys)
    # print(t,x,sgn)
    x -= 1
    if counter[x] == 0:
        s[t] += 1
    counter[x] += sgn
    if counter[x] == 0:
        s[t] -= 1

# print(s)

ans = list(accumulate(s))

print(*ans[1:n+1])