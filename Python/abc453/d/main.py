from collections import deque

# 幅優先探索かも
H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
T = []
direction = [None] * H*W
start = (0,0)
goal = (0,0)
for i in range(H):
    for j in range(W):
        if S[i][j] == "S":
            start = (i,j)
        if S[i][j] == "G":
            goal = (i,j)

queue = deque([start])
visited = set()
while queue:
    node = queue.popleft()
    if node == goal:
        print("Yes")
        break
    (y,x) = node
    if S[y][x] == "." or S[y][x] == "S":
        visited.add(node)
        for (dy,dx) in range([(0,1),(1,0),(-1,0),(0,-1)]):
            ny = y + dy
            nx = x + dx
            if 0 <= nx < W and 0 <= ny < H and S[ny][nx] != "#" and not (ny,nx) in visited:
                queue.append((ny,nx))
                if S[ny][nx] == "." or S[ny][nx] == "G" or S[ny][nx] == "o" or S[ny][nx] == "x":
                    if (dy,dx) == (1,0):
                        direction[ny*W+nx] = "D"
                    elif (dy,dx) == (0,1):
                        direction[ny*W+nx] = "R"
                    elif (dy,dx) == (-1,0):
                        direction[ny*W+nx] = "U"
                    else:
                        direction[ny*W+nx] = "L"
    elif S[y][x] == "x":
        for (dy,dx) in range([(0,1),(1,0),(-1,0),(0,-1)]):
            if (dy,dx) == (0,1) and S[y][x] == "R":
                continue
            elif (dy,dx) == (1,0) and S[y][x] == "D":
                continue
            elif (dy,dx) == (-1,0) and S[y][x] == "U":
                continue
            elif (dy,dx) == (0,-1) and S[y][x] == "L":
                continue
            ny = y + dy
            nx = x + dx
            if 0 <= nx < W and 0 <= ny < H and S[ny][nx] != "#" and not (ny,nx) in visited:
                queue.append((ny,nx))
                if S[ny][nx] == "." or S[ny][nx] == "G" or S[ny][nx] == "o" or S[ny][nx] == "x":
                    if (dy,dx) == (1,0):
                        direction[ny*W+nx] = "D"
                    elif (dy,dx) == (0,1):
                        direction[ny*W+nx] = "R"
                    elif (dy,dx) == (-1,0):
                        direction[ny*W+nx] = "U"
                    else:
                        direction[ny*W+nx] = "L"
    elif S[y][x] == "o":
        for (dy,dx) in range([(0,1),(1,0),(-1,0),(0,-1)]):
            if (dy,dx) != (0,1) and S[y][x] == "R":
                continue
            elif (dy,dx) != (1,0) and S[y][x] == "D":
                continue
            elif (dy,dx) != (-1,0) and S[y][x] == "U":
                continue
            elif (dy,dx) != (0,-1) and S[y][x] == "L":
                continue
            ny = y + dy
            nx = x + dx
            if 0 <= nx < W and 0 <= ny < H and S[ny][nx] != "#" and not (ny,nx) in visited:
                queue.append((ny,nx))
                if S[ny][nx] == "." or S[ny][nx] == "G" or S[ny][nx] == "o" or S[ny][nx] == "x":
                    if (dy,dx) == (1,0):
                        direction[ny*W+nx] = "D"
                    elif (dy,dx) == (0,1):
                        direction[ny*W+nx] = "R"
                    elif (dy,dx) == (-1,0):
                        direction[ny*W+nx] = "U"
                    else:
                        direction[ny*W+nx] = "L"
else:
    print("No")

