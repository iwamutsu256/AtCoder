import math
import random
import sys
import time
from dataclasses import dataclass

# グローバル変数の定義
global_start_time = time.time()  # プログラム開始時刻を記録
candidates = []  # 候補の注文リスト
prime_number = 998244353  # ハッシュ計算に使う素数
base = 10007  # ハッシュ計算に使う基数

def get_hash(x: int, y: int, idx: int, tp: int):
    """
    点の座標とインデックスからハッシュ値を計算する関数
    """
    return (x + y * base + idx * pow(base, 2, prime_number) + tp * pow(base, 3, prime_number)) % prime_number

@dataclass
class Point:
    """
    2次元座標上の点を表すクラス
    """
    x: int
    y: int
    
    def dist(self, p: 'Point') -> int:
        """
        2点間のマンハッタン距離を計算する
        
        Args:
            p (Point): 距離を計算する点
            
        Returns:
            int: 2点間のマンハッタン距離
        """
        return abs(self.x - p.x) + abs(self.y - p.y)

@dataclass
class Restaurant(Point):
    """
    レストランを表すクラス
    """
    idx: int
    
    def __hash__(self) -> int:
        return get_hash(self.x, self.y, self.idx, 0)
    
    def __str__(self) -> str:
        return f"Restaurant(x={self.x}, y={self.y}, idx={self.idx})"

@dataclass
class Destination(Point):
    """
    目的地を表すクラス
    """
    idx: int
    
    def __hash__(self) -> int:
        return get_hash(self.x, self.y, self.idx, 1)
    
    def __str__(self) -> str:
        return f"Destination(x={self.x}, y={self.y}, idx={self.idx})"

@dataclass
class Input:
    """
    入力データを表すクラス
    """
    order_count: int
    pickup_count: int
    office: Point
    restaurants: list[Point]
    destinations: list[Point]
    
    @staticmethod
    def read() -> 'Input':
        """
        入力データを読み込む
        
        Returns:
            Input: 読み込んだ入力データ
        """
        order_count = 1000
        pickup_count = 50
        office = Point(400, 400)
        restaurants = []
        destinations = []
        
        for _ in range(order_count):
            a, b, c, d = map(int, input().split())
            restaurants.append(Point(a, b))
            destinations.append(Point(c, d))
        
        return Input(order_count, pickup_count, office, restaurants, destinations)

@dataclass
class Output:
    """
    出力データを表すクラス
    """
    dist_sum: int
    orders: list[int]
    route: list[Point]
    
    def __init__(self, orders: list[int], route: list[Point]):
        """
        出力データを構築する
        
        Args:
            orders (list[int]): 選択した注文のリスト
            route (list[Point]): 配達ルート
        """
        self.orders = list(orders)
        self.route = list(route)
        
        # 移動距離の合計を計算する
        self.dist_sum = 0
        
        for i in range(len(route) - 1):
            self.dist_sum += route[i].dist(route[i + 1])
    
    def print_output(self):
        """
        解を出力する
        """
        # 選択した注文の集合を出力する
        print(len(self.orders), end=" ")
        
        # 0-indexed -> 1-indexedに変更
        print(" ".join(map(lambda x: str(x + 1), self.orders)))
        
        # 配達ルートを出力する
        print(len(self.route), end="")
        
        for p in self.route:
            print(f" {p.x} {p.y}", end="")
            
        print()

def solve_greedy(input_data: Input, selected_orders: list[int]) -> Output:
    """
    貪欲法で問題を解く関数
    
    Args:
        input_data (Input): 入力データ
        selected_orders (list[int]): 選択した注文のリスト
        
    Returns:
        Output: 出力データ
    """
    route = []  # 配達ルート
    
    current_position = Point(400, 400) # 現在地はオフィス
    visitables = {
        Restaurant(
            input_data.restaurants[i].x,
            input_data.restaurants[i].y,
            i
        ) for i in selected_orders
    }
    route.append(current_position)
    
    __i = 1
    
    while visitables:
        min_dist = 10**9
        next_position = None
        for visitable in visitables:
            if current_position.dist(visitable) < min_dist:
                min_dist = current_position.dist(visitable)
                next_position = visitable
        
        route.append(next_position)
        
        if isinstance(next_position, Restaurant):
            idx = next_position.idx
            visitables.add(Destination(input_data.destinations[idx].x, input_data.destinations[idx].y, next_position.idx))
        
        visitables.remove(next_position)
        current_position = next_position
        
        __i += 1
    
    route.append(Point(400, 400))  # オフィスに帰る
    assert is_valid_order(route)
    return Output(selected_orders, route)

def is_valid_order(route: list[Point]) -> bool:
    """
    注文が配達可能か判定する関数
    
    Args:
        route (list[Point]): 経路
        
    Returns:
        bool: 配達経路として適切ならTrue、そうでなければFalse
    """
    
    got_restaurants = set()
    for i in range(len(route)):
        if isinstance(route[i], Restaurant):
            got_restaurants.add(route[i].idx)
        if isinstance(route[i], Destination):
            if route[i].idx not in got_restaurants:
                return False
    return True

def get_distance(route: list[Point]) -> int:
    """
    経路の距離を計算する関数
    
    Args:
        route (list[Point]): 経路
        
    Returns:
        int: 経路の距離
    """
    dist = 0
    
    for i in range(len(route) - 1):
        dist += route[i].dist(route[i + 1])
    
    return dist

def update_distance(route: list[Point], i: int, j: int) -> int:
    """
    経路の距離を更新する関数
    
    Args:
        route (list[Point]): 経路
        i (int): 移動前のインデックス
        j (int): 移動後のインデックス
        
    Returns:
        int: 更新後の経路の距離の変化量
    """
    if i == j:
        return 0
    elif i > j:
        before = route[j].dist(route[j-1]) + route[i].dist(route[i-1]) + route[i+1].dist(route[i])
        after = route[i].dist(route[j]) + route[i].dist(route[j-1]) + route[i-1].dist(route[i+1])
    else:
        before = route[j+1].dist(route[j]) + route[i].dist(route[i-1]) + route[i+1].dist(route[i])
        after = route[j+1].dist(route[i]) + route[j].dist(route[i]) + route[i+1].dist(route[i-1])    
    return after - before

def update_index(destination_dict: dict[int], restaurant_dict: dict[int], i: int, j: int):
    """
    レストランと配達先のインデックスを更新する関数
    
    Args:
        destination_dict (dict[int]): 配達先のインデックス辞書
        restaurant_dict (dict[int]): レストランのインデックス辞書
        i (int): 移動前のインデックス
        j (int): 移動後のインデックス
    """
    if i < j:
        for key in destination_dict:
            if destination_dict[key] > i and destination_dict[key] <= j:
                destination_dict[key] -= 1
        for key in restaurant_dict:
            if restaurant_dict[key] > i and restaurant_dict[key] <= j:
                restaurant_dict[key] -= 1
    elif i > j:
        for key in destination_dict:
            if destination_dict[key] < i and destination_dict[key] >= j:
                destination_dict[key] += 1
        for key in restaurant_dict:
            if restaurant_dict[key] < i and restaurant_dict[key] >= j:
                restaurant_dict[key] += 1
    return

def solve_order_annealing(input_data: Input, output_data_greedy: Output) -> Output:
    """
    注文の選択を焼きなまし法で最適化する関数
    
    Args:
        input_data (Input): 入力データ
        output_data_greedy (Output): 貪欲法で求めた出力データ
        
    Returns:
        Output: 最適化された出力データ
    """
    orders = set(output_data_greedy.orders)
    route = list(output_data_greedy.route)
    current_dist = get_distance(route)
    
    # 開始温度と終了温度
    start_temperature = 50
    end_temperature = 1
    
    # 現在の温度
    current_temperature = start_temperature
    
    # 制限時間
    time_limit = 1.2
    start_time = time.time()
    
    # 試行回数
    iteration = 0
    random.seed(998244353)
    
    while True:
        # 現在時刻を取得
        current_time = time.time()
        
        # 制限時間になったら終了
        if current_time - global_start_time >= time_limit:
            break
        
        i = random.choice(list(orders))
        j = random.choice(candidates)

        while j in orders:
            j = random.choice(candidates)
        
        orders.remove(i)
        orders.add(j)
        
        output = solve_greedy(input_data, list(orders))
        new_dist = get_distance(output.route)
        
        if new_dist <= current_dist or random.random() <= math.exp((current_dist - new_dist) / current_temperature):
            current_dist = new_dist
        else:
            orders.remove(j)
            orders.add(i)
        
        # 試行回数のカウントを増やす
        iteration += 1
        if iteration % 1000 == 0:
            print(f"iteration: {iteration}, total distance: {current_dist}", file=sys.stderr)
        
        # 現在の経過時間の割合を計算する
        progress = (current_time - start_time) / time_limit
        # 温度の更新
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
    print(f"iteration: {iteration}, total_distance: {current_dist}",file=sys.stderr)
    return solve_greedy(input_data, list(orders))

def solve_route_simulated_annealing(input_data: Input, output_data_order_annealing: Output) -> Output:
    """
    配達先の訪問順序を焼きなまし法で改善する関数
    
    Args:
        input_data (Input): 入力データ
        output_data_order_annealing (Output): 注文選択の焼きなまし法で求めた出力データ
        
    Returns:
        Output: 経路最適化された出力データ
    """
    # 初期解のコピー
    orders = list(output_data_order_annealing.orders)
    route = list(output_data_order_annealing.route)
    
    # 現在の経路の距離を計算
    current_dist = get_distance(route)
    
    # 乱数生成器のシード値を設定
    random.seed(42)
    
    # 焼きなまし法の開始時刻を取得
    start_time = time.time()
    
    # 制限時間を残りの時間から計算
    time_limit = 1.8 - (start_time - global_start_time)
    
    # 開始温度と終了温度
    start_temperature = 3e1
    end_temperature = 1e0
    
    # 現在の温度
    current_temperature = start_temperature
    
    # 試行回数
    iteration = 0
    
    # レストランと配達先のインデックスを追跡するための辞書を作成
    restaurant_dict = {order: route.index(Restaurant(input_data.restaurants[order].x, input_data.restaurants[order].y, order)) for order in orders}
    destination_dict = {order: route.index(Destination(input_data.destinations[order].x, input_data.destinations[order].y, order)) for order in orders}
    
    # 焼きなまし法の本体
    while time.time() - start_time < time_limit:
        rand_orders = random.choice(orders)
        
        if iteration & 1:  # レストランを選んで配達先よりも前に挿入
            i = restaurant_dict[rand_orders]
            j = random.randint(1, destination_dict[rand_orders]-1)
            
            # 経路の距離の変化を計算
            delta = update_distance(route, i, j)
            
            if delta <= 0 or random.random() < math.exp(-delta / current_temperature):
                update_index(destination_dict, restaurant_dict, i, j)
                restaurant_dict[rand_orders] = j
                point_to_move = route.pop(i)
                route.insert(j, point_to_move)
                current_dist += delta
        else:  # 配達先を選んでレストランよりも後に挿入
            i = destination_dict[rand_orders]
            j = random.randint(restaurant_dict[rand_orders]+1, len(route)-2)
            
            # 経路の距離の変化を計算
            delta = update_distance(route, i, j)
            
            if delta <= 0 or random.random() < math.exp(-delta / current_temperature):
                update_index(destination_dict, restaurant_dict, i, j)
                destination_dict[rand_orders] = j
                point_to_move = route.pop(i)
                route.insert(j, point_to_move)
                current_dist += delta
        
        # 試行回数のカウントを増やす
        iteration += 1
        if iteration % 1000 == 0:
            print(f"iteration: {iteration}, total distance: {current_dist}", file=sys.stderr)
        
        # 現在の経過時間の割合を計算する
        progress = (time.time() - start_time) / time_limit
        # 温度の更新
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
    
    # 試行回数と合計距離を標準エラー出力に出力
    print("--- Route Simulated Annealing Result ---", file=sys.stderr)
    print("iteration     :", iteration, file=sys.stderr)
    print("total distance:", current_dist, file=sys.stderr)
    
    return Output(orders, route)

def main():
    """
    メイン関数
    """
    global candidates
    # 入力データを受け取る
    input_data = Input.read()
    global global_start_time
    global_start_time = time.time()
    
    # 問題を解く
    # 注文を距離に基づいてソート
    sorted_orders = sorted(
        range(input_data.order_count), 
        key=lambda i: max(
            Point(400, 400).dist(input_data.restaurants[i]),
            Point(400, 400).dist(input_data.destinations[i])
        )
    )
    
    # 候補注文の選択
    candidates = sorted_orders[:3 * input_data.pickup_count]
    
    # 最初の注文選択
    first_selected_orders = sorted_orders[:input_data.pickup_count]
    
    # 貪欲法で初期解を取得
    output_data_greedy = solve_greedy(input_data, first_selected_orders)
    
    # 注文選択の焼きなまし法
    output_data_order_annealing = solve_order_annealing(input_data, output_data_greedy)
    
    # 経路の焼きなまし法
    output_data = solve_route_simulated_annealing(input_data, output_data_order_annealing)
    
    # 出力する
    output_data.print_output()

if __name__ == "__main__":
    main()