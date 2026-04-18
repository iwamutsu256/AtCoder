from collections import deque, defaultdict
N,M = map(int,input().split())
exchange = defaultdict(list)
for _ in range(M):
    A,B = map(int,input().split())
    exchange[A].append(B)
getItemCount = 1
geted = [False for _ in range(N+1)]
geted[1] = True
queue = deque([1])
while queue:
    item = queue.popleft()
    for can_exchange in exchange[item]:
        if not geted[can_exchange]:
            queue.append(can_exchange)
            geted[can_exchange] = True
            getItemCount += 1
print(getItemCount)
    
