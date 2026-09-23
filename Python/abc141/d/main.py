import heapq

n,m = map(int,input().split())
a = list(map(int,input().split()))

queue = []
heapq.heapify(queue)

for i in range(n):
    heapq.heappush(queue,-a[i])

for i in range(m):
    item = -heapq.heappop(queue)
    item /= 2
    heapq.heappush(queue,-item)

ans = 0
for i in range(n):
    ans += -heapq.heappop(queue)//1
print(int(ans))