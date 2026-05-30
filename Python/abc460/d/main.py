from collections import deque
H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
T = [[-1 for _ in range(W)] for _ in range(H)]
queue = deque([])
count = 0
for i in range(H):
    for j in range(W):
        if S[i][j] == "#":
            T[i][j] = 0
            queue.append((i,j,0))
else:
    while count < H*W and queue:
        y,x,s = queue.popleft()
        for (dx, dy) in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H and (T[ny][nx] == -1 or (T[ny][nx] == 0 and s != 0)):
                T[ny][nx] = s+1
                count += 1
                queue.append((ny,nx,s+1))
    # print(T)
    U = [list(map(lambda x: "#" if (x % 2 == 0 and x != 0)else ".",T[i])) for i in range(H)]
    for i in range(H):
        print("".join(U[i]))