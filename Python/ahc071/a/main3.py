# 各高さでできるだけ長いレンガを使って敷き詰める

w, h, k = map(int,input().split())
cn = map(int,input().split())
holes = [tuple(map(int,input().split())) for _ in range(k)]
# print(holes)
renga_count = 0
renga = []
for i in range(8):
    for j in range(h):
        if i < 6:
            # 中心は(i*9)+4
            if (i*9,j) in holes or (i*9+8,j) in holes:
                renga.append((i*9,j,9))
            elif (i*9+1, j) in holes or (i*9+7,j) in holes:
                renga.append((i*9+1,j,7))
            elif (i*9+2, j) in holes or (i*9+6,j) in holes:
                renga.append((i*9+2,j,5))
            elif (i*9+3, j) in holes or (i*9+5,j) in holes:
                renga.append((i*9+3,j,3))
            else:
                renga.append((i*9+4,j,1))
            renga_count += 1
        else:
            if (54+(i-6)*3,j) in holes or (56+(i-6)*3,j) in holes:
                renga.append((54+(i-6)*3,j,3))
            else:
                renga.append((55+(i-6)*3,j,1))
            renga_count += 1

print(renga_count)
for i in range(renga_count):
    print(*renga[i])