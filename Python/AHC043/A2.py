import heapq
import time
grid = [[-1 for _ in range(50)] for _ in range(50)]
INF = float("inf")
#グリッドの状態
EMPTY = -1
STATION = 0
RAIL_HORIZONTAL = 1
RAIL_VERTICAL = 2
RAIL_LEFT_DOWN = 3
RAIL_LEFT_UP = 4
RAIL_RIGHT_UP = 5
RAIL_RIGHT_DOWN = 6
#コスト
COST_STATION = 5000
COST_RAIL = 100

##ダイクストラ法が使えそう
##やっぱりA*法のほうがよさそう


#2点のマンハッタン距離を返す関数
def manhattan_distance(sx,sy,gx,gy):
    return abs(sx-gx)+abs(sy-gy)

#2点間の最小コストを返す関数
def a_star(grid, sx, sy, gx, gy):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右の4方向
    open_set = []
    # 初期位置のコストとマンハッタン距離を優先度付きキューに追加
    heapq.heappush(open_set, (0 + manhattan_distance(sx, sy, gx, gy), 0, sx, sy))
    cost_so_far = {(sx, sy): 0}
    came_from = {(sx, sy): None}
    turns = 0
    
    while open_set:
        # 最小コストのノードを取り出す
        _, current_cost, x, y = heapq.heappop(open_set)
        
        # ゴールに到達した場合、コストと経路を返す
        if (x, y) == (gx, gy):
            path = []
            turns = 0
            empty_flag = True
            while came_from[(x, y)] is not None:
                path.append((x, y))
                if grid[x][y] > 0 and empty_flag:
                    turns += 1
                if grid[x][y] == EMPTY:
                    turns += 1
                    empty_flag = True
                else:
                    empty_flag = False
                x, y = came_from[(x, y)]
            path.append((x,y))
            path.reverse()
            return current_cost, path, turns
        
        # 4方向に移動
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 50 and 0 <= ny < 50:
                # 新しいコストを計算
                if grid[nx][ny] == EMPTY:
                    new_cost = current_cost + COST_RAIL
                elif grid[nx][ny] != STATION and grid[x][y] == EMPTY:
                    new_cost = current_cost + COST_STATION
                else:
                    new_cost = current_cost
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    priority = new_cost + manhattan_distance(nx, ny, gx, gy)
                    heapq.heappush(open_set, (priority, new_cost, nx, ny))
                    came_from[(nx, ny)] = (x, y)
    
    return INF, [], 0  # 経路が見つからなかった場合


def culuculate_cost(turn):
    # 各人の家と職場の間に線路を設置するときのコストを計算して出力
    top_5 = []
    for i in range(M):
        sx, sy = home[i]
        gx, gy = workspace[i]
        cost, path, turns = a_star(grid, sx, sy, gx, gy)
        if cost == INF:
            continue
        cost += 9900
        turns += 1
        gain = manhattan_distance(sx, sy, gx, gy)
        total_gain = (801 - (turn + turns)) * gain - cost
        if len(top_5) < 5:
            top_5.append([i, cost, turns, path, gain, total_gain])
            top_5.sort(key=lambda x: x[5], reverse=True)
        elif total_gain > top_5[-1][5]:
            top_5[-1] = [i, cost, turns, path, gain, total_gain]
            top_5.sort(key=lambda x: x[5], reverse=True)
    return top_5

def build_railway(path,K):
    empty_flag = False
    for i in range(len(path)):
        if i == 0 or i == len(path)-1:
            grid[path[i][0]][path[i][1]] = STATION
            print(0,path[i][0],path[i][1])
            K -= COST_STATION
        elif grid[path[i][0]][path[i][1]] > 0 and empty_flag:
            grid[path[i][0]][path[i][1]] = STATION
            print(0,path[i][0],path[i][1])
            K -= COST_STATION
        else:
            if grid[path[i][0]][path[i][1]] == EMPTY:
                empty_flag = True
            else:
                empty_flag = False
            dx = path[i+1][0] - path[i-1][0]
            dy = path[i+1][1] - path[i-1][1]
            dx1 = path[i][0] - path[i-1][0]
            dy1 = path[i][1] - path[i-1][1]
            dx2 = path[i+1][0] - path[i][0]
            dy2 = path[i+1][1] - path[i][1]
            if (dx,dy) == (0,2) or (dx,dy) == (0,-2):
                grid[path[i][0]][path[i][1]] = RAIL_HORIZONTAL
                print(1,path[i][0],path[i][1])
                K -= COST_RAIL
            elif (dx,dy) == (2,0) or (dx,dy) == (-2,0):
                grid[path[i][0]][path[i][1]] = RAIL_VERTICAL
                print(2,path[i][0],path[i][1])
                K -= COST_RAIL
            elif (dx1,dy2) == (-1,-1) or (dx2,dy1) == (1,1):
                grid[path[i][0]][path[i][1]] = RAIL_LEFT_DOWN
                print(3,path[i][0],path[i][1])
                K -= COST_RAIL
            elif (dx1,dy2) == (1,-1) or (dx2,dy1) == (-1,1):
                grid[path[i][0]][path[i][1]] = RAIL_LEFT_UP
                print(4,path[i][0],path[i][1])
                K -= COST_RAIL
            elif (dx1,dy2) == (1,1) or (dx2,dy1) == (-1,-1):
                grid[path[i][0]][path[i][1]] = RAIL_RIGHT_UP
                print(5,path[i][0],path[i][1])
                K -= COST_RAIL
            elif (dx1,dy2) == (-1,1) or (dx2,dy1) == (1,-1):
                grid[path[i][0]][path[i][1]] = RAIL_RIGHT_DOWN
                print(6,path[i][0],path[i][1])
                K -= COST_RAIL
            else:
                print(-1)
    return K


def execute_person(turn):
    Person_info = culuculate_cost(turn)
    for info in Person_info:
        if info[1] <= K:
            return info
    return -1

N, M, K, T = map(int, input().split())
home = []
workspace = []
turn = 0
start_time = time.time()
for _ in range(M):
    i0s, j0s, i0t, j0t = map(int, input().split())
    home.append((i0s, j0s))
    workspace.append((i0t, j0t))

while turn < T:
    Person_info = execute_person(turn)
    if Person_info == -1:
        for i in range(T-turn):
            print(-1)
        turn = T
    else:
        K = build_railway(Person_info[3],K)
        turn += Person_info[2]

end_time = time.time()
print(f"time = {end_time-start_time}sec")
