N = int(input())
points = [list(map(int,input().split())) for _ in range(N)]
points.sort()
# print(points)
height = N+1
count = 0
for i in range(1,N+1):
    if points[i-1][1] < height:
        count += 1
        height = points[i-1][1]
print(count)