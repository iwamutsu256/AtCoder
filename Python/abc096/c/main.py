import sys
h,w = map(int,input().split())
s = [list(input()) for _ in range(h)]

for i in range(h):
    for j in range(w):
        if s[i][j] == ".":
            continue
        flag = False
        for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            ny,nx = i+dy, j+dx
            if 0 <= ny < h and 0 <= nx < w and s[ny][nx] == "#":
                flag = True
        if not flag:
            print("No")
            sys.exit()
else:
    print("Yes")
