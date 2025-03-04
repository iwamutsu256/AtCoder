from collections import deque
Q = int(input())
T = deque()
minus_count = 0
for i in range(Q):
    query = [int(x) for x in input().split()]
    #print(query)
    if query[0] == 1:
        if len(T) > 0:
            T.append([T[-1][0]+T[-1][1],query[1]])
        else:
            T.append([0,query[1]])
        #print(T)
    elif query[0] == 2:
        minus_count += T[0][1]
        T.popleft()
        #print(T)
    else:
        print(T[query[1]-1][0] - minus_count)
