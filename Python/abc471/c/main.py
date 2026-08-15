import heapq
n = int(input())
a = list(map(int,input().split()))
left = [10**10+1]
right = [10**10+1]
for i in range(n):
    if a[i] >= 0:
        heapq.heappush(right, a[i])
    else:
        heapq.heappush(left, -a[i])

pos = 0
dist_sum = 0 
right_pos = heapq.heappop(right)
left_pos = -heapq.heappop(left)
for i in range(n):
    if abs(right_pos-pos) == abs(left_pos-pos):
        dist_sum += abs(left_pos-pos)
        pos = left_pos
        left_pos = -heapq.heappop(left)
    elif abs(right_pos-pos) > abs(left_pos-pos):
        dist_sum += abs(left_pos-pos)
        pos = left_pos
        left_pos = -heapq.heappop(left)
    else:
        dist_sum += abs(right_pos-pos)
        pos = right_pos
        right_pos = heapq.heappop(right)
print(dist_sum)