from collections import deque
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

#駅と駅を結ぶ関数
def connect_station(sx,sy,gx,gy):
    global turn
    global K
    if sx < gx:
        for i in range(gx-sx-1):
            print(RAIL_VERTICAL,sx+i+1,sy)
            grid[sx+i+1][sy] = RAIL_VERTICAL
        K -= (gx-sx-1)*COST_RAIL
        turn += gx-sx-1
        K += (gx-sx-1)*income
    elif sx > gx:
        for i in range(sx-gx-1):
            print(RAIL_VERTICAL,gx+i+1,sy)
            grid[gx+i+1][sy] = RAIL_VERTICAL
        K -= (sx-gx-1)*COST_RAIL
        turn += sx-gx-1
        K += (sx-gx-1)*income
    else:
        pass
    if sy < gy:
        for i in range(gy-sy-1):
            print(RAIL_HORIZONTAL,gx,sy+i+1)
            grid[gx][sy+i+1] = RAIL_HORIZONTAL
        K -= (gy-sy-1)*COST_RAIL
        turn += gy-sy-1
        K += (gy-sy-1)*income
    elif sy > gy:
        for i in range(sy-gy-1):
            print(RAIL_HORIZONTAL,gx,gy+i+1)
            grid[gx][gy+i+1] = RAIL_HORIZONTAL
        K -= (sy-gy-1)*COST_RAIL
        turn += sy-gy-1
        K += (sy-gy-1)*income
    else:
        pass
    if sy != gy and sx != gx:
        if sy < gy and sx < gx:
            print(RAIL_RIGHT_UP,gx,sy)
            grid[gx][sy] = RAIL_RIGHT_UP
            K -= COST_RAIL
            turn += 1
            K += income
        elif sy < gy and sx > gx:
            print(RAIL_RIGHT_DOWN,gx,sy)
            grid[gx][sy] = RAIL_RIGHT_DOWN
            K -= COST_RAIL
            turn += 1
            K += income
        elif sy > gy and sx < gx:
            print(RAIL_LEFT_UP,gx,sy)
            grid[gx][sy] = RAIL_LEFT_UP
            K -= COST_RAIL
            turn += 1
            K += income
        else:
            print(RAIL_LEFT_DOWN,gx,sy)
            grid[gx][sy] = RAIL_LEFT_DOWN
            K -= COST_RAIL
            turn += 1
            K += income
    return

#収入を再計算する関数
def reculuculate_income():
    global income
    income = 0
    for item in railway_done:
        income += distance[item]
    return


#駅周辺の探索候補を追加する関数
def add_candidate(x,y):
    candidate = neighbors(x,y)
    global cand_home
    global cand_workspace
    global railway_done
    for item in candidate:
        cand_home.update(home_point[item[0]][item[1]])
        cand_workspace.update(workspace_point[item[0]][item[1]])
    railway_done.update(cand_home&cand_workspace)
    cand_home -= railway_done
    cand_workspace -= railway_done
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
    K -= COST_STATION*2
    station_position.append((msg[0],msg[1]))
    station_position.append((msg[2],msg[3]))
    add_candidate(msg[0],msg[1])
    add_candidate(msg[2],msg[3])
    print(0,msg[0],msg[1])
    print(0,msg[2],msg[3])
    turn += 2
    K += 2*income
    return msg

#任意の点と最寄りの駅との距離を返す関数
def distation(x,y):
    minimum = 1000
    for item in station_position:
        if manhattan_distance(x,y,item[0],item[1]) < minimum:
            minimum = manhattan_distance(x,y,item[0],item[1])
            sta_pos_x = item[0]
            sta_pos_y = item[1]
    return [minimum,sta_pos_x,sta_pos_y]


#候補の家や職場を探索する関数
#候補のうち、(最長)最短のものを選ぶ
def search_candidate():
    global turn
    global K
    global cand_home
    global cand_workspace
    global railway_done
    sta = None
    cand = None
    lists = []
    for item in cand_home:
        lists.append(distation(workspace[item][0],workspace[item][1]))
        lists[-1].append(workspace[item][0])
        lists[-1].append(workspace[item][1])
        #if lists[0] < minimum:
        #    minimum = lists[0]
        #    sta = lists
        #    cand = [workspace[item][0],workspace[item][1]]
    for item in cand_workspace:
        lists.append(distation(home[item][0],home[item][1]))
        lists[-1].append(home[item][0])
        lists[-1].append(home[item][1])
        #if lists[0] < minimum:
        #    minimum = lists[0]
        #    sta = lists
        #    cand = [home[item][0],home[item][1]]
    lists.sort()
    deques = deque(lists)
    if len(deques) == 0:
        print(-1)
        return
    score = K + income*(T-turn)
    for i in range(len(deques)):
        new_score = K - COST_STATION - COST_RAIL*deques[0][0] + (income+deques[0][0])*(T-turn-deques[0][0]) + deques[0][0]*income
        if K+income*deques[0][0] >= COST_STATION+COST_RAIL*(deques[0][0]-1):
            if new_score > score:
                connect_station(deques[0][1],deques[0][2],deques[0][3],deques[0][4])
                #駅の建設のほうが後
                K -= COST_STATION
                station_position.append((deques[0][3],deques[0][4]))
                add_candidate(deques[0][3],deques[0][4])
                print(0,deques[0][3],deques[0][4])
                turn += 1
                reculuculate_income()
                K += income
                return
            else:
                deques.popleft()
        else:
            need_turn = ((COST_STATION+COST_RAIL*(deques[0][0]-1)-(K+income*deques[0][0]))//income)+1
            for _ in range(need_turn):
                print(-1)
            turn += need_turn
            return


N, M, K, T = map(int, input().split())
#i番目には人iの家と職場の座標が入っている
income = 0
home = []
workspace = []
distance = []
station_position = []
#候補の家と職場のインデックスを保存する集合(候補とは駅の周囲2マス以内にある線路でつながれていない家や職場)
cand_home = set()
cand_workspace = set()
#すでにつなぎ終わった家や職場のインデックスを保存する集合
railway_done = set()
#グリッド上のそれぞれの座標に家や職場があるかどうかの配列
home_point = [[set() for _ in range(50)] for _ in range(50)]
workspace_point = [[set() for _ in range(50)] for _ in range(50)]
turn = 0
#入力の受け取りと保存
for i in range(M):
    home_x, home_y, workspace_x, workspace_y = map(int, input().split())
    home.append((home_x, home_y))
    workspace.append((workspace_x, workspace_y))
    distance.append(manhattan_distance(home_x,home_y,workspace_x,workspace_y))
    home_point[home_x][home_y].add(i)
    workspace_point[workspace_x][workspace_y].add(i)

#タイマースタート
start_time = time.time()

#メイン関数
sta = first_station(K)
connect_station(sta[0],sta[1],sta[2],sta[3])
reculuculate_income()
while turn < T:
    search_candidate()
    #print(f"#turn = {turn}")
print(f"K = {K}")
#タイマーストップ
end_time = time.time()
print(f"\ntime = {end_time-start_time}sec")