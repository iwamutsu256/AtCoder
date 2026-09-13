# 各高さでできるだけ長いレンガを使って敷き詰める

w, h, k = map(int,input().split())
cn = map(int,input().split())
holes = [list(map(int,input().split())) for _ in range(k)]

renga_count = 0
renga = []
for i in range(8):
    for j in range(h):
        if i < 6:
            renga.append((i*9,j,9))
            renga_count += 1
        else:
            renga.append((54+(i-6)*3,j,3))
            renga_count += 1

print(renga_count)
for i in range(renga_count):
    print(*renga[i])