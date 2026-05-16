import heapq

X = int(input())
Q = int(input())
left = []
right = []
heapq.heappush(left,float('inf'))
heapq.heappush(right, float('inf'))
heapq.heappush(left, -X)
# center = X
for _ in range(Q):
    A,B = map(int,input().split())
    left_max = -heapq.heappop(left)
    right_min = heapq.heappop(right)
    if A < left_max:
        heapq.heappush(right, right_min)
        heapq.heappush(right, left_max)
        heapq.heappush(left, -A)
    else:
        heapq.heappush(right, right_min)
        heapq.heappush(right, A)
        heapq.heappush(left, -left_max)
    left_max = -heapq.heappop(left)
    right_min = heapq.heappop(right)
    if B > right_min:
        heapq.heappush(left, -left_max)
        heapq.heappush(left, -right_min)
        heapq.heappush(right, B)
    else:
        heapq.heappush(left, -left_max)
        heapq.heappush(left, -B)
        heapq.heappush(right, right_min)

    left_max = -heapq.heappop(left)
    right_min = heapq.heappop(right)
    if len(left) > len(right):
        print(left_max)
    else:
        print((left_max + right_min) // 2)
    heapq.heappush(left,-left_max)
    heapq.heappush(right, right_min)