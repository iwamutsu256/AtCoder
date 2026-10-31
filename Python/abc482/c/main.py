import bisect

h,w,n,q = map(int,input().split())
komas = [tuple(map(int,input().split())) for _ in range(n)]

gyou = []
retsu = []

for i in range(n):
    y,x = komas[i]
    gyou.append(y)
    retsu.append(x)

gyou.sort()
retsu.sort()

for _ in range(q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        u,d = query[1],query[2]
        start = bisect.bisect_left(gyou,u)
        end = bisect.bisect_right(gyou,d)
        print(end-start)
    else:
        l,r = query[1],query[2]
        start = bisect.bisect_left(retsu,l)
        end = bisect.bisect_right(retsu,r)
        print(end-start)