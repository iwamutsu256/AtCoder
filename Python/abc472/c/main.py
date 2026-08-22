from collections import deque
n,m,k = map(int,input().split())
a = list(map(int,input().split()))
queue = deque()
sum = 0
for i in range(n):
    # print(sum+a[i])
    if sum + a[i] <= k:
        print("Yes")
        queue.append(a[i])
        sum += a[i]
    else:
        print("No")
        queue.append(0)
    if len(queue) >= m:
        dust = queue.popleft()
        sum -= dust
