from collections import deque
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

def manhattan_distance(sx, sy, gx, gy):
    return abs(sx - gx) + abs(sy - gy)

class Field:
    def __init__(self, N):
        self.N = N
        self.grid = [[EMPTY for _ in range(50)] for _ in range(50)]
        self.home_point = [[set() for _ in range(50)] for _ in range(50)]
        self.workspace_point = [[set() for _ in range(50)] for _ in range(50)]
        self.station_position = []
        self.cand_home = set()
        self.cand_workspace = set()
        self.railway_done = set()

    def neighbors(self, x, y):
        neighbor = set()
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if abs(dx) + abs(dy) <= 2:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 50 and 0 <= ny < 50:
                        neighbor.add((nx, ny))
        return neighbor

    def add_candidate(self, x, y):
        candidate = self.neighbors(x, y)
        for item in candidate:
            self.cand_home.update(self.home_point[item[0]][item[1]])
            self.cand_workspace.update(self.workspace_point[item[0]][item[1]])
        self.railway_done.update(self.cand_home & self.cand_workspace)
        self.cand_home -= self.railway_done
        self.cand_workspace -= self.railway_done

    def grid_pos_point(self, x, y, distance):
        point = 0
        neighbor = self.neighbors(x, y)
        for item in neighbor:
            for i in self.home_point[item[0]][item[1]]:
                point += distance[i]
            for i in self.workspace_point[item[0]][item[1]]:
                point += distance[i]
        return point

    def distation(self, x, y):
        minimum = 1000
        for item in self.station_position:
            if manhattan_distance(x, y, item[0], item[1]) < minimum:
                minimum = manhattan_distance(x, y, item[0], item[1])
                sta_pos_x = item[0]
                sta_pos_y = item[1]
        return [minimum, sta_pos_x, sta_pos_y]

    def connect_station(self, sx, sy, gx, gy, K, turn, income):
        if sx < gx:
            for i in range(gx - sx - 1):
                print(RAIL_VERTICAL, sx + i + 1, sy)
                self.grid[sx + i + 1][sy] = RAIL_VERTICAL
            K -= (gx - sx - 1) * COST_RAIL
            turn += gx - sx - 1
            K += (gx - sx - 1) * income
        elif sx > gx:
            for i in range(sx - gx - 1):
                print(RAIL_VERTICAL, gx + i + 1, sy)
                self.grid[gx + i + 1][sy] = RAIL_VERTICAL
            K -= (sx - gx - 1) * COST_RAIL
            turn += sx - gx - 1
            K += (sx - gx - 1) * income
        if sy < gy:
            for i in range(gy - sy - 1):
                print(RAIL_HORIZONTAL, gx, sy + i + 1)
                self.grid[gx][sy + i + 1] = RAIL_HORIZONTAL
            K -= (gy - sy - 1) * COST_RAIL
            turn += gy - sy - 1
            K += (gy - sy - 1) * income
        elif sy > gy:
            for i in range(sy - gy - 1):
                print(RAIL_HORIZONTAL, gx, gy + i + 1)
                self.grid[gx][gy + i + 1] = RAIL_HORIZONTAL
            K -= (sy - gy - 1) * COST_RAIL
            turn += sy - gy - 1
            K += (sy - gy - 1) * income
        if sy != gy and sx != gx:
            if sy < gy and sx < gx:
                print(RAIL_RIGHT_UP, gx, sy)
                self.grid[gx][sy] = RAIL_RIGHT_UP
                K -= COST_RAIL
                turn += 1
                K += income
            elif sy < gy and sx > gx:
                print(RAIL_RIGHT_DOWN, gx, sy)
                self.grid[gx][sy] = RAIL_RIGHT_DOWN
                K -= COST_RAIL
                turn += 1
                K += income
            elif sy > gy and sx < gx:
                print(RAIL_LEFT_UP, gx, sy)
                self.grid[gx][sy] = RAIL_LEFT_UP
                K -= COST_RAIL
                turn += 1
                K += income
            else:
                print(RAIL_LEFT_DOWN, gx, sy)
                self.grid[gx][sy] = RAIL_LEFT_DOWN
                K -= COST_RAIL
                turn += 1
                K += income
        return K, turn

class Solver:
    def __init__(self, N, M, K, T, home, workspace):
        self.N = N
        self.M = M
        self.K = K
        self.T = T
        self.home = home
        self.workspace = workspace
        self.distance = [manhattan_distance(home[i][0], home[i][1], workspace[i][0], workspace[i][1]) for i in range(M)]
        self.field = Field(N)
        self.turn = 0
        self.income = 0
        self.start_time = time.time()

    def reculuculate_income(self):
        self.income = 0
        for item in self.field.railway_done:
            self.income += self.distance[item]

    def first_station(self):
        maximum = 0
        for i in range(self.M):
            if self.distance[i] <= ((self.K - COST_STATION * 2) // COST_RAIL) + 5:
                start = set()
                goal = set()
                for item in self.field.neighbors(self.home[i][0], self.home[i][1]):
                    start.add(item)
                for item in self.field.neighbors(self.workspace[i][0], self.workspace[i][1]):
                    goal.add(item)
                for j in start:
                    for k in goal:
                        if manhattan_distance(j[0], j[1], k[0], k[1]) <= ((self.K - COST_STATION * 2) // COST_RAIL) + 1:
                            if self.distance[i] * (self.field.grid_pos_point(j[0], j[1], self.distance) + self.field.grid_pos_point(k[0], k[1], self.distance)) > maximum:
                                maximum = self.distance[i] * (self.field.grid_pos_point(j[0], j[1], self.distance) + self.field.grid_pos_point(k[0], k[1], self.distance))
                                msg = [j[0], j[1], k[0], k[1]]
            else:
                pass
        self.K -= COST_STATION * 2
        self.field.station_position.append((msg[0], msg[1]))
        self.field.station_position.append((msg[2], msg[3]))
        self.field.add_candidate(msg[0], msg[1])
        self.field.add_candidate(msg[2], msg[3])
        print(0, msg[0], msg[1])
        print(0, msg[2], msg[3])
        self.turn += 2
        self.K += 2 * self.income
        return msg

    def search_candidate(self):
        lists = []
        for item in self.field.cand_home:
            lists.append(self.field.distation(self.workspace[item][0], self.workspace[item][1]))
            lists[-1].append(self.workspace[item][0])
            lists[-1].append(self.workspace[item][1])
        for item in self.field.cand_workspace:
            lists.append(self.field.distation(self.home[item][0], self.home[item][1]))
            lists[-1].append(self.home[item][0])
            lists[-1].append(self.home[item][1])
        lists.sort()
        deques = deque(lists)
        if len(deques) == 0:
            print(-1)
            return
        score = self.K + self.income * (self.T - self.turn)
        for i in range(len(deques)):
            new_score = self.K - COST_STATION - COST_RAIL * deques[0][0] + (self.income + deques[0][0]) * (self.T - self.turn - deques[0][0]) + deques[0][0] * self.income
            if self.K + self.income * deques[0][0] >= COST_STATION + COST_RAIL * (deques[0][0] - 1):
                if new_score > score:
                    self.K, self.turn = self.field.connect_station(deques[0][1], deques[0][2], deques[0][3], deques[0][4], self.K, self.turn, self.income)
                    self.K -= COST_STATION
                    self.field.station_position.append((deques[0][3], deques[0][4]))
                    self.field.add_candidate(deques[0][3], deques[0][4])
                    print(0, deques[0][3], deques[0][4])
                    self.turn += 1
                    self.reculuculate_income()
                    self.K += self.income
                    return
                else:
                    deques.popleft()
            else:
                need_turn = ((COST_STATION + COST_RAIL * (deques[0][0] - 1) - (self.K + self.income * deques[0][0])) // self.income) + 1
                for _ in range(need_turn):
                    print(-1)
                self.turn += need_turn
                return

    def run(self):
        for i in range(self.M):
            self.field.home_point[self.home[i][0]][self.home[i][1]].add(i)
            self.field.workspace_point[self.workspace[i][0]][self.workspace[i][1]].add(i)

        sta = self.first_station()
        self.K, self.turn = self.field.connect_station(sta[0], sta[1], sta[2], sta[3], self.K, self.turn, self.income)
        self.reculuculate_income()
        while self.turn < self.T:
            self.search_candidate()
        print(f"K = {self.K}")
        end_time = time.time()
        print(f"\ntime = {end_time - self.start_time}sec")


def main():
    N, M, K, T = map(int, input().split())
    home = []
    workspace = []
    for _ in range(M):
        home_x, home_y, workspace_x, workspace_y = map(int, input().split())
        home.append((home_x, home_y))
        workspace.append((workspace_x, workspace_y))

    solver = Solver(N, M, K, T, home, workspace)
    solver.run()

if __name__ == "__main__":
    main()
