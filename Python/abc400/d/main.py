# 幅優先探索
H,W = map(int,input().split())
# 0-indexed
S = [list(input()) for _ in range(H)]
# 1-indexed
A,B,C,D = map(int,input().split())
queue = []
visited = [[False for _ in range(W)] for _ in range(H)]
# ４つ目の要素は前回前下痢をどの方向にしたか
queue.append((0,A-1,B-1,0))
visited[A-1][B-1] = True
while queue:
    cost,x,y,kick = queue.pop(0)
    if (x,y) == (C-1,D-1):
        print(cost)
        exit()
    for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
        nx,ny = x+dx,y+dy
        # Sが.であればコストが0,#であれば、コストが1
        if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny]:
            if S[nx][ny] == "#":
                if kick == 0:
                    if (dx,dy) == (0,1):
                        queue.append((cost+1,nx,ny,1))
                    elif (dx,dy) == (1,0):
                        queue.append((cost+1,nx,ny,2))
                    elif (dx,dy) == (0,-1):
                        queue.append((cost+1,nx,ny,3))
                    else:
                        queue.append((cost+1,nx,ny,4))
                    visited[nx][ny] = True
                else:
                    if kick == 1 and (dx,dy) == (0,1):
                        queue.append((cost,nx,ny,0))
                    elif kick == 2 and (dx,dy) == (1,0):
                        queue.append((cost,nx,ny,0))
                    elif kick == 3 and (dx,dy) == (0,-1):
                        queue.append((cost,nx,ny,0))
                    elif kick == 4 and (dx,dy) == (-1,0):
                        queue.append((cost,nx,ny,0))
                    elif (dx,dy) == (0,1):
                        queue.append((cost+1,nx,ny,1))
                    elif (dx,dy) == (1,0):
                        queue.append((cost+1,nx,ny,2))
                    elif (dx,dy) == (0,-1):
                        queue.append((cost+1,nx,ny,3))
                    else:
                        queue.append((cost+1,nx,ny,4))
                    visited[nx][ny] = True
            else:
                queue.append((cost,nx,ny,0))
                visited[nx][ny] = True
            # コストが低いものから順に探索
            queue.sort()
else:
    print(-1)