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

def manhattan_distance(sx,sy,gx,gy):
    return abs(sx-gx)+abs(sy-gy)

#ある点の近傍の点を返す関数
def neighbors(x,y):
    neighbor = set()
    for dx in range(-2,3):
        for dy in range(-2,3):
            if abs(dx)+abs(dy)<=2:
                nx,ny = x+dx,y+dy
                if 0<=nx<50 and 0<=ny<50:
                    neighbor.add((nx,ny))
    return neighbor

#始点と終点を与えてその路線で得られる利益を返す関数
def s_to_g_cost(sx,sy,gx,gy):
    house = set()
    work = set()
    for item in neighbors(sx,sy):
        for i in home_point[item[0]][item[1]]:
            house.add(i)
        for i in workspace_point[item[0]][item[1]]:
            work.add(i)
    for item in neighbors(gx,gy):
        for i in home_point[item[0]][item[1]]:
            house.add(i)
        for i in workspace_point[item[0]][item[1]]:
            work.add(i)
    both = house & work
    profit = 0
    for item in both:
        profit += distance[item]
    return profit

#ある点に駅を置いたときにその周囲の家や職場の通勤距離を得点として返す関数
def grid_pos_point(x,y):
    point = 0
    neighbor = neighbors(x,y)
    for item in neighbor:
        for i in home_point[item[0]][item[1]]:
            point += distance[i]
        for i in workspace_point[item[0]][item[1]]:
            point += distance[i]
    return point

def connect_station(sx,sy,gx,gy):
    global turn
    if sx < gx:
        for i in range(gx-sx-1):
            print(RAIL_VERTICAL,sx+i+1,sy)
            grid[sx+i+1][sy] = RAIL_VERTICAL
            turn += 1
    elif sx > gx:
        for i in range(sx-gx-1):
            print(RAIL_VERTICAL,gx+i+1,sy)
            grid[gx+i+1][sy] = RAIL_VERTICAL
            turn += 1
    else:
        pass
    if sy < gy:
        for i in range(gy-sy-1):
            print(RAIL_HORIZONTAL,gx,sy+i+1)
            grid[gx][sy+i+1] = RAIL_HORIZONTAL
            turn += 1
    elif sy > gy:
        for i in range(sy-gy-1):
            print(RAIL_HORIZONTAL,gx,gy+i+1)
            grid[gx][gy+i+1] = RAIL_HORIZONTAL
            turn += 1
    else:
        pass
    if sy != gy and sx != gx:
        if sy < gy and sx < gx:
            print(RAIL_RIGHT_UP,gx,sy)
            grid[gx][sy] = RAIL_RIGHT_UP
            turn += 1
        elif sy < gy and sx > gx:
            print(RAIL_RIGHT_DOWN,gx,sy)
            grid[gx][sy] = RAIL_RIGHT_DOWN
            turn += 1
        elif sy > gy and sx < gx:
            print(RAIL_LEFT_UP,gx,sy)
            grid[gx][sy] = RAIL_LEFT_UP
            turn += 1
        else:
            print(RAIL_LEFT_DOWN,gx,sy)
            grid[gx][sy] = RAIL_LEFT_DOWN
            turn += 1
    return
#最初の路線を引く関数
def first_station(K):
    global turn
    maximum = 0
    for i in range(M):
        if distance[i]<= ((K-COST_STATION*2)//COST_RAIL)+5:
            start = set()
            goal = set()
            for item in neighbors(home[i][0],home[i][1]):
                start.add(item)
            for item in neighbors(workspace[i][0],workspace[i][1]):
                goal.add(item)
            for j in start:
                for k in goal:
                    if manhattan_distance(j[0],j[1],k[0],k[1]) <= ((K-COST_STATION*2)//COST_RAIL)+1:
                        if distance[i]*(grid_pos_point(j[0],j[1])+grid_pos_point(k[0],k[1]))>maximum:
                            maximum = distance[i]*(grid_pos_point(j[0],j[1])+grid_pos_point(k[0],k[1]))
                            msg = [j[0],j[1],k[0],k[1]]
        else:
            pass
    print(0,msg[0],msg[1])
    print(0,msg[2],msg[3])
    turn += 2
    return msg


N, M, K, T = map(int, input().split())
#i番目には人iの家と職場の座標が入っている
home = []
workspace = []
distance = []
#グリッド上のそれぞれの座標に家や職場があるかどうかの配列
home_point = [[set() for _ in range(50)] for _ in range(50)]
workspace_point = [[set() for _ in range(50)] for _ in range(50)]
global turn
turn = 0
start_time = time.time()
for i in range(M):
    home_x, home_y, workspace_x, workspace_y = map(int, input().split())
    home.append((home_x, home_y))
    workspace.append((workspace_x, workspace_y))
    distance.append(manhattan_distance(home_x,home_y,workspace_x,workspace_y))
    home_point[home_x][home_y].add(i)
    workspace_point[workspace_x][workspace_y].add(i)

station = first_station(K)
connect_station(station[0],station[1],station[2],station[3])
for _ in range(T-turn):
    print(-1)

end_time = time.time()
#print(f"\ntime = {end_time-start_time}sec")