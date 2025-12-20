import heapq
T = int(input())
for _ in range(T):
    N = int(input())
    array = []
    sum = 0
    for i in range(N):
        W,P = map(int,input().split())
        heapq.heappush(array,(-abs(W+P),W,P))
        sum += W
    power = 0
    count = N
    while sum > power:
        _,w,p =heapq.heappop(array)
        sum -= w
        power += p
        count  -= 1
    print(count)