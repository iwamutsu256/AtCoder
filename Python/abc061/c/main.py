import heapq,sys

n,k = map(int,input().split())

queue = []
heapq.heapify(queue)

for i in range(n):
    a,b = map(int,input().split())
    heapq.heappush(queue,(a,b))

for i in range(n):
    a,b = heapq.heappop(queue)
    # print(b)
    if b >= k:
        print(a)
        sys.exit()
    k -= b