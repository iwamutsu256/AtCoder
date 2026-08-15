import heapq
q,v = map(int,input().split())
battery = []
for _ in range(q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        heapq.heappush(battery, -(query[2]-query[1]))
    else:
        if len(battery) == 0:
            print(-1)
        else:
            print(min(-heapq.heappop(battery)+query[1],v))
    # print(battery)