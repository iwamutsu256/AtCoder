import heapq
N,M = map(int,input().split())
P = [int(x) for x in input().split()]
T = []
for i in range(N):
    heapq.heappush(T,[P[i],1,P[i]])
sam = 0
count = 0
while sam <= M:
    #print(T)
    temp = heapq.heappop(T)
    #print(temp)
    sam += temp[0]
    heapq.heappush(T,[temp[2]*(2*(temp[1]+1)-1),(temp[1]+1),temp[2]])
    count += 1
    #print(sam,temp[0])
print(count-1)