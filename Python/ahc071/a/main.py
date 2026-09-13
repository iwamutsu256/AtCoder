# すべてのマスに長さ1のレンガを配置

w, h, k = map(int,input().split())
cn = map(int,input().split())
holes = [list(map(int,input().split())) for _ in range(k)]

renga_count = 0
renga = []
for i in range(w):
    for j in range(h):
        renga.append((i,j,1))
        renga_count += 1

print(renga_count)
for i in range(renga_count):
    print(*renga[i])