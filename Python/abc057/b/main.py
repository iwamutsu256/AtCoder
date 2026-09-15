def dist(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

n,m = map(int,input().split())
students = [tuple(map(int,input().split())) for _ in range(n)]
checks = [tuple(map(int,input().split())) for _ in range(m)]

for i in range(n):
    point = -1
    distance = 10**10
    x1,y1 = students[i]
    for j in range(m):
        x2,y2 = checks[j]
        new_dist = dist(x1,y1,x2,y2)
        if distance > new_dist:
            distance = new_dist
            point = j+1
    print(point)