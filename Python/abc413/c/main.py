from collections import deque

nums = deque()
counters = deque()
Q = int(input())
for i in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        nums.append(query[2])
        counters.append(query[1])
    else:
        count = 0
        sum = 0
        while count != query[1]:
            if counters[0] <= query[1]-count:
                sum += nums[0]*counters[0]
                count += counters[0]
                nums.popleft()
                counters.popleft()
            else:
                sum += nums[0]*(query[1]-count)
                counters[0] -= query[1]-count
                count = query[1]
        print(sum)
