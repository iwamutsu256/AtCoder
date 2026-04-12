#最新版　動作は良いが実行時間がオーバーする(33/50がTLE)

from collections import deque
import heapq
import sys
import time

Pos = tuple[int,int]
EMPTY = -1
STATION = 0
RAIL_HORIZONTAL = 1
RAIL_VERTICAL = 2
RAIL_LEFT_DOWN = 3
RAIL_LEFT_UP = 4
RAIL_RIGHT_UP = 5
RAIL_RIGHT_DOWN = 6
COST_STATION = 5000
COST_RAIL = 100
INF = float("inf")
DO_NOTHING = -1

#このクラスでは線路の連結性を管理する
class UnionFind:
    def __init__(self, n: int):
        self.n = n
        self.parents = [-1 for _ in range(n * n)]

    def _find_root(self, idx: int) -> int:
        if self.parents[idx] < 0:
            return idx
        self.parents[idx] = self._find_root(self.parents[idx])
        return self.parents[idx]

    def is_same(self, p: Pos, q: Pos) -> bool:
        p_idx = p[0] * self.n + p[1]
        q_idx = q[0] * self.n + q[1]
        return self._find_root(p_idx) == self._find_root(q_idx)

    def unite(self, p: Pos, q: Pos) -> None:
        p_idx = p[0] * self.n + p[1]
        q_idx = q[0] * self.n + q[1]
        p_root = self._find_root(p_idx)
        q_root = self._find_root(q_idx)
        if p_root != q_root:
            p_size = -self.parents[p_root]
            q_size = -self.parents[q_root]
            if p_size > q_size:
                p_root, q_root = q_root, p_root
            self.parents[q_root] += self.parents[p_root]
            self.parents[p_root] = q_root


def manhattan_distance(s:Pos,g:Pos):
    return abs(s[0]-g[0])+abs(s[1]-g[1])

#このクラスでは盤面の管理のみを行う
class Field:
    def __init__(self,N: int,distance:list[int],home_point:list[list[set]],workspace_point:list[list[set]]):
        self.N = N
        self.grid = [[EMPTY for _ in range(N)] for _ in range(N)]
        self.home_point = home_point
        self.workspace_point = workspace_point
        self.station_pos = []
        self.cand_home = set()
        self.cand_workspace = set()
        self.railway_done = set()
        self.uf = UnionFind(N)
        self.distance = distance

    #線路又は駅を盤面に設置する関数
    def build(self, type: int, r: int, c: int):
        #assert は条件が偽の時にデバッグで止まってくれる関数
        assert self.grid[r][c] != STATION
        if 1 <= type <= 6:
            assert self.grid[r][c] == EMPTY
        if type == STATION:
            self.station_pos.append((r,c))
        self.grid[r][c] = type
        # 隣接する区画と接続
        # 上
        if type in (STATION, RAIL_VERTICAL, RAIL_LEFT_UP, RAIL_RIGHT_UP):
            if r > 0 and self.grid[r - 1][c] in (STATION, RAIL_VERTICAL, RAIL_LEFT_DOWN, RAIL_RIGHT_DOWN):
                self.uf.unite((r, c), (r - 1, c))
        # 下
        if type in (STATION, RAIL_VERTICAL, RAIL_LEFT_DOWN, RAIL_RIGHT_DOWN):
            if r < self.N - 1 and self.grid[r + 1][c] in (STATION, RAIL_VERTICAL, RAIL_LEFT_UP, RAIL_RIGHT_UP):
                self.uf.unite((r, c), (r + 1, c))
        # 左
        if type in (STATION, RAIL_HORIZONTAL, RAIL_LEFT_DOWN, RAIL_LEFT_UP):
            if c > 0 and self.grid[r][c - 1] in (STATION, RAIL_HORIZONTAL, RAIL_RIGHT_DOWN, RAIL_RIGHT_UP):
                self.uf.unite((r, c), (r, c - 1))
        # 右
        if type in (STATION, RAIL_HORIZONTAL, RAIL_RIGHT_DOWN, RAIL_RIGHT_UP):
            if c < self.N - 1 and self.grid[r][c + 1] in (STATION, RAIL_HORIZONTAL, RAIL_LEFT_DOWN, RAIL_LEFT_UP):
                self.uf.unite((r, c), (r, c + 1))

    #ある地点ともう一方の地点が駅の範囲に含まれていてなおかつ連結されているかどうか
    def is_connected(self, s: Pos, t: Pos) -> bool:
        assert manhattan_distance(s, t) > 4  # 前提条件
        stations0 = self.collect_stations(s)
        stations1 = self.collect_stations(t)
        for station0 in stations0:
            for station1 in stations1:
                if self.uf.is_same(station0, station1):
                    return True
        return False

    #ある点の近傍の駅を返す関数
    def collect_stations(self, pos: Pos) -> list[Pos]:
        stations = []
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if abs(dr) + abs(dc) > 2:
                    continue
                r = pos[0] + dr
                c = pos[1] + dc
                if 0 <= r < self.N and 0 <= c < self.N and self.grid[r][c] == STATION:
                    stations.append((r, c))
        return stations

    #ある点の近傍の点を返す関数
    def neighbors(self,Pos):
        neighbor = set()
        for dx in range(-2,3):
            for dy in range(-2,3):
                if abs(dx)+abs(dy) <= 2:
                    nx,ny = Pos[0]+dx,Pos[1]+dy
                    if 0 <= nx < self.N and 0 <= ny < self.N:
                        neighbor.add((nx,ny))
        return neighbor
    
    #2点間の最短距離と経路を返す関数
    def a_star(self,s:Pos,g:Pos):
        if self.grid[s[0]][s[1]] != EMPTY and self.grid[s[0]][s[1]] != STATION:
            return INF,[],0
        if self.grid[g[0]][g[1]] != EMPTY and self.grid[g[0]][g[1]] != STATION:
            return INF,[],0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        open_set = []
        heapq.heappush(open_set, (0 + manhattan_distance(s,g), 0, s[0], s[1]))
        cost_so_far = {s: 0}
        came_from = {s: None}
        while open_set:
            # 最小コストのノードを取り出す
            _, current_cost, x, y = heapq.heappop(open_set)
            # ゴールに到達した場合、距離と経路を返す
            if (x, y) == g:
                path = []
                while came_from[(x, y)] is not None:
                    path.append((x, y))
                    x, y = came_from[(x, y)]
                path.append(s)
                path.reverse()
                return current_cost, path, len(path)
        
            # 4方向に移動
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < 50 and 0 <= ny < 50 and self.grid[nx][ny] == EMPTY) or (0 <= nx < 50 and 0 <= ny < 50 and self.grid[nx][ny] == STATION and ((nx,ny) == s or (nx,ny) == g)):
                    # 新しいコストを計算
                    new_cost = current_cost + 1
                    if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                        cost_so_far[(nx, ny)] = new_cost
                        priority = new_cost + manhattan_distance((nx, ny), g)
                        heapq.heappush(open_set, (priority, new_cost, nx, ny))
                        came_from[(nx, ny)] = (x, y)
        return INF, [], 0  # 経路が見つからなかった場合
    
    #ある点に駅を置いたときにその周囲の家や職場の通勤距離を得点として返す関数
    def grid_pos_point(self,x,y):
        point = 0
        neighbor = self.neighbors((x,y))
        for item in neighbor:
            for i in self.home_point[item[0]][item[1]]:
                point += self.distance[i]
            for i in self.workspace_point[item[0]][item[1]]:
                point += self.distance[i]
        return point

    #ある点から一番近くにある駅の位置を返す関数
    def nearest_station(self,Pos):
        minimum = 1000
        for item in self.station_pos:
            if manhattan_distance(Pos, item) < minimum:
                minimum = manhattan_distance(Pos, item)
                sta_pos = item
        return sta_pos

    def get_cand_home(self):
        cand_home = set()
        for item in self.station_pos:
            for i in self.neighbors(item):
                cand_home.update(self.home_point[i[0]][i[1]])
        self.cand_home = cand_home
        return


    def get_cand_workspace(self):
        cand_workspace = set()
        for item in self.station_pos:
            for i in self.neighbors(item):
                cand_workspace.update(self.workspace_point[i[0]][i[1]])
        self.cand_workspace = cand_workspace
        return

    def calc_cand(self):
        self.get_cand_home()
        self.get_cand_workspace()
        cand = self.cand_home & self.cand_workspace
        self.cand_home -= cand
        self.cand_workspace -= cand
        return
    
    
class Action:
    def __init__(self, type: int, pos: Pos):
        self.type = type
        self.pos = pos

    def __str__(self):
        if self.type == DO_NOTHING:
            return "-1"
        else:
            return f"{self.type} {self.pos[0]} {self.pos[1]}"


class Result:
    def __init__(self, actions: list[Action], score: int):
        self.actions = actions
        self.score = score

    def __str__(self):
        return "\n".join(map(str, self.actions))
    
class Solver:
    def __init__(self, N: int, M: int, K: int, T: int, home:list[Pos], workspace:list[Pos],distance:list[int],home_point:list[list[set]],workspace_point:list[list[set]]):
        self.N = N
        self.M = M
        self.T = T
        self.money = K
        self.home = home
        self.workspace = workspace
        self.field = Field(N,distance,home_point,workspace_point)
        self.distance = distance
        self.home_point = home_point
        self.workspace_point = workspace_point
        self.turn = 0
        self.income = 0
        self.actions = []

    def turn_progress(self):
        self.turn += 1
        self.calc_income()
        self.money += self.income

    def calc_income(self) -> int:
        income = 0
        for i in range(self.M):
            if self.field.is_connected(self.home[i], self.workspace[i]):
                income += manhattan_distance(self.home[i], self.workspace[i])
        self.income = income

    def build_rail(self,type:int, x:int, y:int):
        self.field.build(type,x,y)
        self.money -= COST_RAIL
        self.actions.append(Action(type, (x,y)))
        self.turn_progress()


    def build_station(self, x: int, y: int):
        self.field.build(STATION, x, y)
        self.money -= COST_STATION
        self.actions.append(Action(STATION,(x,y)))
        self.turn_progress()

    def build_nothing(self):
        self.actions.append(Action(DO_NOTHING,(0,0)))
        self.turn_progress()

    def first_station(self):
        maximum = 0
        msg = None  # 初期化
        for i in range(self.M):
            if self.distance[i] <= ((self.money - COST_STATION * 2) // COST_RAIL) + 5:
                start = set()
                goal = set()
                for item in self.field.neighbors(self.home[i]):
                    start.add(item)
                for item in self.field.neighbors(self.workspace[i]):
                    goal.add(item)
                for j in start:
                    for k in goal:
                        if manhattan_distance(j, k) <= ((self.money - COST_STATION * 2) // COST_RAIL) + 1:
                            if self.distance[i] * (self.field.grid_pos_point(j[0], j[1]) + self.field.grid_pos_point(k[0], k[1])) > maximum:
                                maximum = self.distance[i] * (self.field.grid_pos_point(j[0], j[1]) + self.field.grid_pos_point(k[0], k[1]))
                                msg = [j, k]
            else:
                pass
        if msg is None:
            raise ValueError("適切な駅の位置が見つかりませんでした。")
        self.build_station(msg[0][0],msg[0][1])
        self.build_station(msg[1][0],msg[1][1])
        #self.field.station_pos.append(msg[0])
        #self.field.station_pos.append(msg[1])
        #self.field.add_candidate(msg[0])
        #self.field.add_candidate(msg[1])
        return msg
    

    #2回目以降の駅を選ぶ関数
    def select_station(self):
        self.field.calc_cand()
        cand_home = self.field.cand_home
        cand_workspace = self.field.cand_workspace
        candidate = []
        for item in cand_home:
            #この駅は固定
            #固定ではないことが発覚
            #その地点から一番近い駅に結んだほうが効率がいい
            #static_station = self.field.collect_stations(self.home[item])
            #こっちの駅建設予定地の周辺を探索
            station = self.field.neighbors(self.workspace[item])
            maximum = 0
            new_score = 0
            sta_pos = (0,0)
            length = 0
            path = []
            nearest_sta = (0,0)
            for i in station:
                nearest_sta = self.field.nearest_station(i)
                #a_starの戻り値がおかしい
                #直した
                _,pre_path,length_path = self.field.a_star(i,nearest_sta)
                if length_path != 0 and self.field.grid_pos_point(i[0],i[1]) > maximum:
                    maximum = self.field.grid_pos_point(i[0],i[1])
                    sta_pos = i
                    length = length_path
                    path = pre_path
                    new_score = self.money-(COST_STATION+COST_RAIL*(length-2))+self.income*(self.T-self.turn)+(801-self.turn-length)*self.field.distance[item]
            if len(candidate) == 0:
                candidate = [new_score,nearest_sta,sta_pos,length,path]
            else:
                if new_score > candidate[0]:
                    candidate = [new_score,nearest_sta,sta_pos,length,path]
        for item in cand_workspace:
            #static_station = self.field.collect_stations(self.workspace[item])
            station = self.field.neighbors(self.home[item])
            maximum = 0
            new_score = 0
            sta_pos = (0,0)
            length = 0
            path = []
            nearest_sta = (0,0)
            for i in station:
                nearest_sta = self.field.nearest_station(i)
                _,pre_path,length_path = self.field.a_star(i,nearest_sta)
                if length_path != 0 and self.field.grid_pos_point(i[0],i[1]) > maximum:
                    maximum = self.field.grid_pos_point(i[0],i[1])
                    sta_pos = i
                    length = length_path
                    path = pre_path
                    new_score = self.money-(COST_STATION+COST_RAIL*(length-2))+self.income*(self.T-self.turn)+(801-self.turn-length)*self.field.distance[item]
            if len(candidate) == 0:
                candidate = [new_score,nearest_sta,sta_pos,length,path]
            else:
                if new_score > candidate[0]:
                    candidate = [new_score,nearest_sta,sta_pos,length,path]
        #候補がcandidateに決まった
        #建設できるなら建設する
        #できないならできるようになるまで待機
        #そもそも利益が出ないなら一生待機
        score = self.money + self.income*(self.T-self.turn)
        if candidate[0] <= score:
            #一生待機
            while len(self.actions) < self.T:
                self.build_nothing()
        else:
            if self.money + self.income*(candidate[3]-2) >= COST_STATION + (candidate[3]+2)*COST_RAIL:
                #建設開始
                #ここのリストの受け渡しがうまくいっていない
                self.build_railway(candidate[4])
                self.build_station(candidate[2][0],candidate[2][1])
            else:
                while self.money + self.income*(candidate[3]-2) < COST_STATION + (candidate[3]+2)*COST_RAIL and len(self.actions) < self.T:
                    self.build_nothing()

    def build_railway(self,p:list):
        path = p
        for i in range(len(path)):
            if i == 0 or i == len(path)-1:
                pass
            else:
                dx = path[i+1][0] - path[i-1][0]
                dy = path[i+1][1] - path[i-1][1]
                dx1 = path[i][0] - path[i-1][0]
                dy1 = path[i][1] - path[i-1][1]
                dx2 = path[i+1][0] - path[i][0]
                dy2 = path[i+1][1] - path[i][1]
                if (dx,dy) == (0,2) or (dx,dy) == (0,-2):
                    self.build_rail(RAIL_HORIZONTAL,path[i][0],path[i][1])
                elif (dx,dy) == (2,0) or (dx,dy) == (-2,0):
                    self.build_rail(RAIL_VERTICAL,path[i][0],path[i][1])
                elif (dx1,dy2) == (-1,-1) or (dx2,dy1) == (1,1):
                    self.build_rail(RAIL_LEFT_DOWN,path[i][0],path[i][1])
                elif (dx1,dy2) == (1,-1) or (dx2,dy1) == (-1,1):
                    self.build_rail(RAIL_LEFT_UP,path[i][0],path[i][1])
                elif (dx1,dy2) == (1,1) or (dx2,dy1) == (-1,-1):
                    self.build_rail(RAIL_RIGHT_UP,path[i][0],path[i][1])
                elif (dx1,dy2) == (-1,1) or (dx2,dy1) == (1,-1):
                    self.build_rail(RAIL_RIGHT_DOWN,path[i][0],path[i][1])
                else:
                    self.build_nothing()
        return


    #直線距離で線路を引く関数
    def connect_station(self,start:Pos,goal:Pos):
        if start[0] < goal[0]:
            for i in range(goal[0]-start[0]-1):
                self.build_rail(RAIL_VERTICAL,start[0]+i+1,start[1])
        elif start[0] > goal[0]:
            for i in range(start[0]-goal[0]-1):
                self.build_rail(RAIL_VERTICAL,goal[0]+i+1,start[1])
        else:
            pass
        if start[1] < goal[1]:
            for i in range(goal[1]-start[1]-1):
                self.build_rail(RAIL_HORIZONTAL,goal[0],start[1]+i+1)
        elif start[1] > goal[1]:
            for i in range(start[1]-goal[1]-1):
                self.build_rail(RAIL_HORIZONTAL,goal[0],goal[1]+i+1)
        else:
            pass
        #ここの接続がおかしいので修正が必要
        #修正完了
        if start[1] != goal[1] and start[0] != goal[0]:
            if start[1] < goal[1] and start[0] < goal[0]:
                self.build_rail(RAIL_RIGHT_UP,goal[0],start[1])
            elif start[1] < goal[1] and start[0] > goal[0]:
                self.build_rail(RAIL_RIGHT_DOWN,goal[0],start[1])
            elif start[1] > goal[1] and start[0] < goal[0]:
                self.build_rail(RAIL_LEFT_UP,goal[0],start[1])
            else:
                self.build_rail(RAIL_LEFT_DOWN,goal[0],start[1])
        return

    def solve(self) -> Result:
        first_station = self.first_station()
        self.connect_station(first_station[0],first_station[1])
        # あとは待機
        while len(self.actions) < self.T:
            #self.build_nothing()
            self.select_station()
        return Result(self.actions, self.money)

def main():
    N, M, K, T = map(int, input().split())
    home = []
    workspace = []
    distance = []
    home_point = [[set() for _ in range(N)] for _ in range(N)]
    workspace_point = [[set() for _ in range(N)] for _ in range(N)]
    for i in range(M):
        home_x, home_y, workspace_x, workspace_y = map(int, input().split())
        home.append((home_x, home_y))
        workspace.append((workspace_x, workspace_y))
        distance.append(manhattan_distance((home_x,home_y),(workspace_x,workspace_y)))
        home_point[home_x][home_y].add(i)
        workspace_point[workspace_x][workspace_y].add(i)
    start_time = time.time()
    solver = Solver(N, M, K, T, home, workspace,distance,home_point,workspace_point)
    result = solver.solve()
    print(result)
    #print(f"score={result.score}", file=sys.stderr)
    end_time = time.time()
    #print(f"time = {end_time - start_time}sec")

if __name__ == "__main__":
    main()