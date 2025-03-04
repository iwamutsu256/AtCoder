def day(t,d):
    if garbage[t][1] >= d % garbage[t][0]:
        d += garbage[t][1] - d % garbage[t][0]
        return d
    else:
        d += garbage[t][0]-(d % garbage[t][0] - garbage[t][1])
        return d

N = int(input())
garbage = []
for i in range(N):
    garbage.append(list(map(int,input().split())))
Q = int(input())
for i in range(Q):
    T,D = map(int,input().split())
    print(day(T-1,D))

