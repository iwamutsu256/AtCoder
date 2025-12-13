from collections import deque
# DFS
def dfs(x,y,count):
    for i,j in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+i, y+j
        if 0 <= nx < H and 0 <= ny < W and S[nx][ny] != "#" and not is_visited[nx][ny]:
            is_visited[nx][ny] = True
            queue.append((nx,ny,count+1))
    c = S[x][y]
    if c != "." and c in keyword_dict:
        for i,j in keyword_dict[c]:
            if not is_visited[i][j]:
                is_visited[i][j] = True
                queue.append((i,j,count+1))
        keyword_dict[c].clear()
    return

H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
is_visited = [[False for _ in range(W)] for _ in range(H)]
is_visited[0][0] = True
keyword_dict = {}
for i in range(H):
    for j in range(W):
        if S[i][j] != "#" and S[i][j] != ".":
            if S[i][j] in keyword_dict:
                keyword_dict[S[i][j]].append((i,j))
            else:
                keyword_dict[S[i][j]] = [(i,j)]
queue = deque([(0,0,0)])
while queue:
    x,y,count = queue.popleft()
    if x == H-1 and y == W-1:
        print(count)
        break
    dfs(x,y,count)
else:
    print(-1)