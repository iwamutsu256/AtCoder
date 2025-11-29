"""次の色と内部状態を、最初に参照されたときに過去改変して決定する。
最短経路上を移動できるような色と内部状態を貪欲にそのつど探索する

複数ある場合の優先度を色々変えてみたらだいぶ改善した

リファクタリングしてる最中に偶然バグ1つが修正されたところ、
盤面の色が偏りやすくなって一部のケースで状態数が増加しすぎるようになってしまった。
(全ケース的にはやや改善?)

色々対策を試したけど悪化しかしない。
唯一、最短経路数が高い方向への移動を優先したら少し改善した。
(同じルールを使用する直線移動の方が優先されるので効果は微妙)

なにやっても改善しないので初期パラメータだけ変えて5回実行するように
"""
from collections import deque

INF = 10 ** 9
DY = [0, 1, 0, -1, 0]
DX = [1, 0, -1, 0, 0]
D5 = list(zip(DY, DX))
D4 = D5[0:4]
D8 = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
CHARS = "RDLUS"
Vec2i = tuple[int, int]


class Info:
    def __init__(self) -> None:
        n, k, t = map(int, input().split())
        self.n = n
        self.k = k
        self.t = t
        self.can_move = [[[False] * 4 for _ in range(self.n)] for _ in range(self.n)]
        for y in range(self.n):
            for x, flag in enumerate(input()):
                if flag == "0":
                    self.can_move[y][x][0] = True
                    self.can_move[y][x + 1][2] = True
        for y in range(self.n - 1):
            for x, flag in enumerate(input()):
                if flag == "0":
                    self.can_move[y][x][1] = True
                    self.can_move[y + 1][x][3] = True
        self.targets = [tuple(map(int, input().split())) for _ in range(self.k)]
        
        self.distances: list[list[list[int]]] = [[]]
        self.path_num: list[list[list[int]]] = [[]]
        for i in range(1, self.k):
            y, x = self.targets[i]
            distances, path_num = self.calc_distances(y, x)
            self.distances.append(distances)
            self.path_num.append(path_num)
    
    def calc_distances(self, target_y: int, target_x: int) -> tuple[list[list[int]], list[list[int]]]:
        distances = [[INF] * self.n for _ in range(self.n)]
        path_num = [[0] * self.n for _ in range(self.n)]
        que = deque()
        que.append((target_y, target_x, 0))
        distances[target_y][target_x] = 0
        path_num[target_y][target_x] = 1
        while que:
            y, x, dist = que.popleft()
            num = path_num[y][x]
            for i, (dy, dx) in enumerate(D4):
                if not self.can_move[y][x][i]:
                    continue
                ny = y + dy
                nx = x + dx
                if distances[ny][nx] < dist + 1:
                    continue
                elif distances[ny][nx] == dist + 1:
                    path_num[ny][nx] += num
                    continue
                path_num[ny][nx] = num
                distances[ny][nx] = dist + 1
                que.append((ny, nx, dist + 1))
        return distances, path_num


class State:
    def __init__(self, source: 'Info | State', color_num: int, state_num: int) -> None:
        if isinstance(source, Info):
            self.i = source
            self.init_color = [[-1 for _ in range(self.i.n)] for _ in range(self.i.n)]
            self.color_num = color_num
            self.state_num = state_num
            
            self.rules: dict[tuple[int, int], list[int]] = {(-1, -1): [-1, 0, 4]}
            self.cell_last_rules = [[(-1, -1)] * self.i.n for _ in range(self.i.n)]
            self.last_rule = (-1, -1)
            self.rule_history = [(-1, -1)]
            self.y, self.x = self.i.targets[0]
            self.next_target = 1
        else:
            pass
    
    def get_score(self) -> int:
        return self.color_num + self.state_num
    
    def output(self):
        del self.rules[(-1, -1)]
        
        print(self.color_num, self.state_num, len(self.rules))
        for color_y in self.init_color:
            output = []
            for color_yx in color_y:
                if color_yx == -1:
                    color_yx = 0
                output.append(str(color_yx))
            print(" ".join(output))
        for (c, q), (a, s, d) in self.rules.items():
            if a == -1:
                a = 0
            if s == -1:
                s = 0
            print(c, q, a, s, CHARS[d])
    
    def set_last_color(self, set_color: int) -> None:
        """現在地の色を過去にさかのぼって決定する"""
        cell_last_rule = self.cell_last_rules[self.y][self.x]
        if cell_last_rule[0] == -1:
            self.init_color[self.y][self.x] = set_color
        else:
            self.rules[cell_last_rule][0] = set_color
    
    def set_last_state(self, set_state: int) -> None:
        """現在の状態を過去にさかのぼって決定する"""
        self.rules[self.last_rule][1] = set_state
    
    def get_shortest_directions(self) -> list[int]:
        """最短経路になる移動方向を返す"""
        distances = self.i.distances[self.next_target]
        path_num = self.i.path_num[self.next_target]
        can_moves = []
        direction_to_path_num = [0] * 4
        for i, (dy, dx) in enumerate(D4):
            if not self.i.can_move[self.y][self.x][i]:
                continue
            ny = self.y + dy
            nx = self.x + dx
            if distances[ny][nx] >= distances[self.y][self.x]:
                continue
            can_moves.append(i)
            direction_to_path_num[i] = path_num[ny][nx]
        can_moves.sort(key=lambda a: direction_to_path_num[a], reverse=True)
        return can_moves
    
    def calc_reach_next_control(self, use_color: int, use_state: int) -> bool:
        """指定した状態が、目的地までの最短経路のみを通って、行動が制御可能なターンまで到達できるかどうかを求める"""
        y, x = self.y, self.x
        color, state = use_color, use_state
        
        next_target = self.next_target
        distances = self.i.distances[self.next_target]
        target_y, target_x = self.i.targets[next_target]
        
        cell_last_color = dict()  # only overwrite
        while True:
            # ルールが自由に選べる場合、次のターンに内部状態が選択可能になるのでOK
            if (color, state) not in self.rules:
                return True
            n_color, n_state, direction = self.rules[(color, state)]
            # 移動できない場合
            if not self.i.can_move[y][x][direction]:
                return False
            ny = y + DY[direction]
            nx = x + DX[direction]
            color, state = n_color, n_state
            # 最短経路を外れたらダメ
            if distances[ny][nx] >= distances[y][x]:
                return False
            
            # ターン更新
            cell_last_color[(y, x)] = color
            y = ny
            x = nx
            cell_last_rule = self.cell_last_rules[y][x]
            if (y, x) in cell_last_color:
                color = cell_last_color[(y, x)]
            else:
                # まだ訪れたことが無いマスで色が決定されているのは現在ターンの場所のみ
                # その場合はcell_last_colorに代入されてるので確認不要
                color = self.rules[cell_last_rule][0]
            # 現在の色か内部状態が選択可能ならOK
            if color == -1 or state == -1:
                return True
            if y == target_y and x == target_x:
                next_target += 1
                if next_target >= self.i.k:
                    return True
                distances = self.i.distances[next_target]
                target_y, target_x = self.i.targets[next_target]
    
    def search_usable_pair(self, fixed_color: int, fixed_state: int) -> tuple[int, int]:
        """使用可能な現在の状態と次の移動方向を探す"""
        # 使用済みルールを優先するようにしたら最適な優先度も変わった
        # ルールのkey または valueの登場回数, ランダム, 現在の色の出現数(色のみ)
        # ランダム以外はあんまり差が無い
        counter_color = [0] * self.color_num
        counter_state = [0] * self.state_num
        for color, state in self.rules:
            if color >= 0:
                counter_color[color] += 1
            if state >= 0:
                counter_state[state] += 1
        
        if fixed_color == -1:
            candidate_colors = sorted(range(self.color_num), key=lambda a: counter_color[a])
        else:
            candidate_colors = [fixed_color]
        
        if fixed_state == -1:
            candidate_states = sorted(range(self.state_num), key=lambda a: counter_state[a])
        else:
            candidate_states = [fixed_state]
        
        # 使用可能な組み合わせを探索
        # 使用済みルールを優先する
        unused_rule: Vec2i | None = None
        try:
            for color in candidate_colors:
                if fixed_color == -1:
                    self.set_last_color(color)
                for state in candidate_states:
                    if (color, state) not in self.rules:
                        if unused_rule is None:
                            unused_rule = (color, state)
                        continue
                    if fixed_state == -1:
                        self.set_last_state(state)
                    if self.calc_reach_next_control(color, state):
                        return color, state
        finally:
            if fixed_color == -1:
                self.set_last_color(-1)
            if fixed_state == -1:
                self.set_last_state(-1)
        
        if unused_rule is not None:
            return unused_rule
        
        if fixed_state != -1 or (fixed_color == -1 and self.color_num < self.state_num):
            # 新しい色
            fixed_color = self.color_num
            self.color_num += 1
            if fixed_state == -1:
                fixed_state = 0
            return fixed_color, fixed_state
        else:
            # 新しい状態
            fixed_state = self.state_num
            self.state_num += 1
            if fixed_color == -1:
                fixed_color = 0
            return fixed_color, fixed_state
    
    def solve(self):
        # debug用
        # last_choice = (-1, -1, -1)
        
        while self.next_target < self.i.k:
            use_color = self.rules[self.cell_last_rules[self.y][self.x]][0]
            use_state = self.rules[self.last_rule][1]
            use_pair = (use_color, use_state)
            if use_color == -1 or use_state == -1:
                color, state = self.search_usable_pair(use_color, use_state)
                # last_choice = (self.y, self.x, self.next_target)
                
                # 色と状態を過去改変
                if use_color == -1:
                    self.set_last_color(color)
                    use_color = color
                if use_state == -1:
                    self.set_last_state(state)
                    use_state = state
                use_pair = (use_color, use_state)
            
            if use_pair not in self.rules:
                # 適切な方向を計算
                direct = self.get_shortest_directions()[0]
                # ルール作成
                self.rules[use_pair] = [-1, -1, direct]
            else:
                # ルールから移動方向読み取り
                _, _, direct = self.rules[use_pair]
                # assert self.i.can_move[self.y][self.x][direct]
                # ny = self.y + DY[direct]
                # nx = self.x + DX[direct]
                # distances = self.i.distances[self.next_target]
                # assert distances[ny][nx] < distances[self.y][self.x]
            
            self.cell_last_rules[self.y][self.x] = use_pair
            self.last_rule = use_pair
            self.rule_history.append(use_pair)
            
            self.y += DY[direct]
            self.x += DX[direct]
            if (self.y, self.x) == self.i.targets[self.next_target]:
                self.next_target += 1


def main():
    info = Info()
    state = State(info, 1, 1)
    state.solve()
    states = [state]
    already_parameter = {1}
    for i in range(4):
        next_init_num = max((state.color_num + state.state_num) // 4, 1)
        while next_init_num in already_parameter:
            next_init_num -= 1
            if next_init_num == 0:
                next_init_num = max(already_parameter) + 1
        state = State(info, next_init_num, next_init_num)
        state.solve()
        states.append(state)
        already_parameter.add(next_init_num)
    state = min(states, key=lambda s: s.get_score())
    state.output()


main()
