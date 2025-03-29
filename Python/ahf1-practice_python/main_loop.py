"""
注文の焼きなまし後、ルートの焼きなまし
"""

import math
import random
import sys
import time
from dataclasses import dataclass

# 開始時刻を取得
global_start_time = time.time()
candidates = []
prime_number = 998244353
base = 10007

def get_hash(x: int, y: int, idx: int, tp: int):
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
    
    Attributes:
        order_count (int): レストランの数 (=1000)
        pickup_count (int): 選択する必要のある注文の数 (=50)
        office (Point): AtCoderオフィスの座標 (=(400, 400))
        restaurants (list[Point]): レストランの座標の配列
        destinations (list[Point]): 目的地の座標の配列
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
    
    Attributes:
        dist_sum (int): 移動距離の合計
        orders (list[int]): 選択した注文のリスト
        route (list[Point]): 配達ルート
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
    問題を解く関数（この関数を実装していきます）
    
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
    注文が配達可能か判定する
    
    Args:
        order (int): 注文
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
    経路の距離を計算する
    
    Args:
        route (list[Point]): 経路
        
    Returns:
        int: 経路の距離
    """
    dist = 0
    
    for i in range(len(route) - 1):
        dist += route[i].dist(route[i + 1])
    
    return dist

def solve_efficient_annealing(input_data: Input, output_data_greedy: Output) -> Output:
    """
    効率的な焼きなまし法で経路を最適化する関数
    """
    # 初期解の取得
    current_orders = set(output_data_greedy.orders)
    current_route = output_data_greedy.route
    current_dist = get_distance(current_route)
    
    # 最良解の追跡用変数
    best_orders = list(current_orders)
    best_route = current_route
    best_dist = current_dist
    
    # 焼きなまし法のパラメータ
    start_temperature = 50
    end_temperature = 1
    current_temperature = start_temperature
    
    # 時間制限
    time_limit = 1.5
    start_time = time.time()
    
    # 乱数シードの設定
    random.seed(42)
    iteration = 0
    
    while time.time() - global_start_time < time_limit:
        # ランダムに削除する注文と追加する注文を選択
        remove_order = random.choice(list(current_orders))
        add_order = random.choice(candidates)
        
        while add_order in current_orders:
            add_order = random.choice(candidates)
        
        # 新しい注文セットの作成
        new_orders = current_orders.copy()
        new_orders.remove(remove_order)
        new_orders.add(add_order)
        
        # 新しい経路の生成と距離計算
        output = solve_greedy(input_data, list(new_orders))
        new_dist = get_distance(output.route)
        
        # 受理基準
        if new_dist <= current_dist or random.random() <= math.exp((current_dist - new_dist) / current_temperature):
            current_orders = new_orders
            current_route = output.route
            current_dist = new_dist
            
            # 最良解の更新
            if current_dist < best_dist:
                best_dist = current_dist
                best_route = current_route
                best_orders = list(current_orders)
        
        # 温度の更新
        progress = (time.time() - start_time) / time_limit
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
        
        iteration += 1
        if iteration % 1000 == 0:
            print(f"iteration: {iteration}, total distance: {current_dist}", file=sys.stderr)
    print("---Result---", file=sys.stderr)
    print(f"iteration: {iteration}, total_distance: {best_dist}", file=sys.stderr)
    return Output(best_orders, best_route)


def update_distance(route: list[Point], i: int, j: int) -> int:
    """
    経路の距離を更新する
    
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
        before = route[j].dist(route[j-1])+route[i].dist(route[i-1])+route[i+1].dist(route[i])
        after = route[i].dist(route[j])+route[i].dist(route[j-1])+route[i-1].dist(route[i+1])
    else:
        before = route[j+1].dist(route[j])+route[i].dist(route[i-1])+route[i+1].dist(route[i])
        after = route[j+1].dist(route[i])+route[j].dist(route[i])+route[i+1].dist(route[i-1])    
    return after - before

def update_index(destination_dict: dict[int], restaurant_dict: dict[int], i: int, j: int):
    """
    i番目とj番目の間のレストランと配達先のインデックスを更新する関数
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
    else:
        pass
    return

def solve_simulated_annealing(input_data: Input, output_data_greedy: Output) -> Output:
    """
    配達先の訪問順序を焼きなまし法で改善する関数（この関数を実装していきます）
    
    Args:
        input_data (Input): 入力データ
        output_data_greedy (Output): 貪欲法で求めた出力データ
        
    Returns:
        Output: 出力データ
    """
    # 焼きなまし法
    # 「ある1つの配達先を訪問する順序を、別の場所に入れ替える」操作を繰り返すことで、経路を改善する
    
    # 貪欲法で求めた解をコピー(これを初期解とする)
    orders = list(output_data_greedy.orders)
    route = list(output_data_greedy.route)
    #destination_dict = dict(output_data_greedy.destination_dict)
    #restaurant_dict = dict(output_data_greedy.restaurant_dict)
    #greedy_time = float(output_data_greedy.time)
    
    # 現在の経路の距離を計算
    current_dist = get_distance(route)
    
    #現在の最善解
    best_orders = list(orders)
    best_route = list(route)
    best_dist = current_dist

    # 乱数生成器のシード値を設定
    # 乱数のシード値は固定のものにしておくと、デバッグがしやすくなります
    random.seed(42)
    
    # 焼きなまし法の開始時刻を取得
    start_time = time.time()

    #レストランと配達先のルート中のインデックスの辞書(key=orders,value=route.index)
    restaurant_dict = {order: route.index(Restaurant(input_data.restaurants[order].x, input_data.restaurants[order].y, order)) for order in orders}
    destination_dict = {order: route.index(Destination(input_data.destinations[order].x, input_data.destinations[order].y, order)) for order in orders}
    
    # 制限時間(1.7秒)
    # 2秒ちょうどまでやるとTLEになるので、1.9秒(pypy3で提出する場合は1.7秒)程度にしておくとよい
    time_limit = 1.78-(start_time - global_start_time)
    
    # 開始温度と終了温度
    start_temperature = 1e1
    end_temperature = 1e0
    
    # 現在の温度
    current_temperature = start_temperature
    
    # 試行回数
    iteration = 0
    
    # 焼きなまし法の本体
    while True:
        # 現在時刻を取得
        current_time = time.time()
        
        # 制限時間になったら終了
        if current_time - start_time >= time_limit:
            break
        rand_orders = random.choice(orders)
        if iteration & 1:#レストランを選んで配達先よりも前に挿入
            i = restaurant_dict[rand_orders]
            j = random.randint(1, destination_dict[rand_orders]-1)
            delta = update_distance(route, i, j)
            if delta <= 0 or random.random() < math.exp(-delta / current_temperature):
                update_index(destination_dict, restaurant_dict, i, j)
                restaurant_dict[rand_orders] = j
                point_to_move = route.pop(i)
                route.insert(j, point_to_move)
                current_dist += delta
                if current_dist < best_dist:
                    best_route = route
                    best_dist = current_dist
        else:#配達先を選んでレストランよりも後に挿入
            i = destination_dict[rand_orders]
            j = random.randint(restaurant_dict[rand_orders]+1, 2*input_data.pickup_count)
            delta = update_distance(route, i, j)
            if delta <= 0 or random.random() < math.exp(-delta / current_temperature):
                update_index(destination_dict, restaurant_dict, i, j)
                destination_dict[rand_orders] = j
                point_to_move = route.pop(i)
                route.insert(j, point_to_move)
                current_dist += delta
                if current_dist < best_dist:
                    best_route = route
                    best_dist = current_dist
        # 訪問先が配達先であるようなインデックスの中から、
        # 「i番目の訪問先をj番目に移動」する操作をランダムに選ぶことで、
        # ある配達先を訪れる順序を他の配達先の間に変える
        # 貪欲法で求めた解では、配達先の訪問順序は0-indexedで51番目～100番目であることに注意
        # (AtCoderオフィス、レストラン50軒、配達先50軒、AtCoderオフィスの順に並んでいる)
            
        # 試行回数のカウントを増やす
        # 進行状況を可視化するため、一定回数ごとに現在の試行回数と合計距離を標準エラー出力に出力
        iteration += 1
        if iteration % 1000 == 0:
            print(f"iteration: {iteration}, total distance: {current_dist}", file=sys.stderr)
        
        # 現在の経過時間の割合を計算する
        progress = (current_time - start_time) / time_limit
        # 【穴埋め】温度の更新
        # 【ヒント】現在の経過時間の割合に対する温度は start_temperature ** (1.0 - progress) * end_temperature ** progress で計算できる
        ## put your code here ##
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
        
        # ここまで穴埋めして実行できるようになったら、
        # 開始温度(start_temperature)と終了温度(end_temperature)を変えてみて、実行結果がどう変わるかを確認してみましょう
        
    # 試行回数と合計距離を標準エラー出力に出力
    print("--- Result ---", file=sys.stderr)
    print("iteration     :", iteration, file=sys.stderr)
    print("total distance:", best_dist, file=sys.stderr)
    
    return Output(best_orders, best_route)

def main():
    global candidates
    # 入力データを受け取る
    input_data = Input.read()
    
    # 問題を解く
    sorted_orders = sorted(
        range(input_data.order_count), 
        key=lambda i: max(
            Point(400, 400).dist(input_data.restaurants[i]),
            Point(400, 400).dist(input_data.destinations[i])
        )
    )
    for i in range(input_data.order_count):
        if input_data.office.dist(input_data.restaurants[i]) <= 350 and input_data.office.dist(input_data.destinations[i]) <= 350:
            candidates.append(i)
    #candidates = sorted_orders[:3 * input_data.pickup_count]
    first_selected_orders = sorted_orders[:input_data.pickup_count]
    output_data_greedy = solve_greedy(input_data, first_selected_orders)
    
    output_data_sa = solve_efficient_annealing(input_data, output_data_greedy)
    output_data = solve_simulated_annealing(input_data,output_data_sa)
    # 出力する
    output_data.print_output()

if __name__ == "__main__":
    main()