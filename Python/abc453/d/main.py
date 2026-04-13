from collections import deque

# 幅優先探索かも
H,W = map(int,input().split())
S = [input() for _ in range(H)]
start = [0,0]
goal = [0,0]
for i in range(H):
    for j in range(W):
        if S[i][j] == "S":
            start = [i,j]
        if S[i][j] == "G":
            goal = [i,j]

# 位置と前回動いた方向をセットで状態とし、状態をノードとして幅優先探索をする。
# 状態を(y,x,direction)で定義する
# キューには経路復元用のprev上のインデックスを持たせる
queue = deque([(start[0],start[1],None,None)])
visited = [[[False] * 4 for _ in range(W)] for _ in range(H)]
prevs = []
flag = False
index = 0
moves = [(1,0,"D",0),(0,1,"R",1),(-1,0,"U",2),(0,-1,"L",3)]
while queue:
    node = queue.popleft()
    prevs.append(node)
    if node[0] == goal[0] and node[1] == goal[1]:
        flag = True
        break
    cur_y,cur_x,prev_direction,prev_index = node
    cell = S[cur_y][cur_x]
    for dy,dx,direction,d_idx in moves:
        if cell == "o" and direction != prev_direction:
            continue
        if cell == "x" and direction == prev_direction:
            continue
        ny,nx = cur_y+dy,cur_x+dx
        if 0 <= ny < H and 0 <= nx < W and S[ny][nx] != "#" and not visited[ny][nx][d_idx]:
            queue.append((ny,nx,direction,index))
            visited[ny][nx][d_idx] = True
    index += 1

if flag:
    print("Yes")
    # 経路復元
    # prevsのindexからさかのぼる
    reversed_path = []
    while index != 0:
        reversed_path.append(prevs[index][2])
        index = prevs[index][3]
    path = reversed(reversed_path)
    print("".join(path))
else:
    print("No")