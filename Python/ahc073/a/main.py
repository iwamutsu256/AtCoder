# インプット
n,m,k,t = map(int,input().split())
start = tuple(map(int,input().split()))
distinations = [tuple(map(int,input().split())) for _ in range(m)]

# 方針１
# とりあえず転移無し

cy, cx = start

for i in range(k):
    print(0,0)

for i in range(len(distinations)):
    gy,gx = distinations[i]
    for j in range(abs(gx-cx)):
        if gx > cx:
            print("R")
            cx += 1
        else:
            print("L")
            cx -= 1
    for j in range(abs(gy-cy)):
        if gy > cy:
            print("D")
            cy += 1
        else:
            print("U")
            cy -= 1