from collections import deque
h,w,k = map(int,input().split())
s = [list(input()) for _ in range(h)]
# sの転置
t = list(map(list,list(zip(*s[::-1]))))
# 安全な空マスから多始点幅優先探索
safe_h = []
safe_w = []
for i in range(h):
    if s[i] == ["."]*w:
        safe_h.append(i)
for i in range(w):
    if t[i] == ["."]*h:
        safe_w.append(i)
safe_points = deque()
for i in safe_h:
    for j in safe_w:
        safe_points.append((i,j,0))

dist = [[-1 for _ in range(w)] for _ in range(h)]
for point in safe_points:
    y,x,_ = point
    dist[y][x] = 0
queue = safe_points
count = len(safe_points)
# print(safe_points)
# print(dist)
while queue:
    py, px, d = queue.popleft()
    for (dx, dy) in [(0,1),(1,0),(-1,0),(0,-1)]:
        if 0 <= py+dy < h and 0 <= px+dx < w and dist[py+dy][px+dx] == -1 and s[py+dy][px+dx] != "#" and d+1<=k:
            queue.append((py+dy,px+dx,d+1))
            dist[py+dy][px+dx] = d+1
            count += 1
print(count)