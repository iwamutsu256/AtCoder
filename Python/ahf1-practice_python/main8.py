"""
すべてのレストランと配達先を通る貪欲ルートから一番減少幅が大きい注文番号を繰り返し消していく
のを改良し、+-200以内のすべてのレストランと配達先にしてみる
毎回貪欲するのではなく、その注文の場所を飛ばして回るようにしてみる
"""

import math
import random
import sys
import time
from dataclasses import dataclass

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
        destination_dict (dict[int]): 配達先がルートの何番目にあるかの辞書
        restaurant_dict (dict[int]): レストランがルートの何番目にあるかの辞書
    """
    dist_sum: int
    orders: list[int]
    route: list[Point]
    destination_dict: dict[int]
    restaurant_dict: dict[int]
    time: float
    
    def __init__(self, orders: list[int], route: list[Point], destination_dict: dict[int], restaurant_dict: dict[int], time: float):
        """
        出力データを構築する
        
        Args:
            orders (list[int]): 選択した注文のリスト
            route (list[Point]): 配達ルート
        """
        self.orders = list(orders)
        self.route = list(route)
        self.destination_dict = dict(destination_dict)
        self.restaurant_dict = dict(restaurant_dict)
        self.time = float(time)
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

        print("orders = "+str(len(self.orders)),file=sys.stderr)
            
        print()

def solve_greedy(input_data: Input, select_orders: list[int]) -> Output:
    """
    問題を貪欲法で解く関数
    
    Args:
        input_data (Input): 入力データ
        
    Returns:
        Output: 出力データ
    """
    # 貪欲その2
    # 以下を順に実行するプログラム
    # 1.オフィスから距離400以下の注文だけを候補にする
    # 2.高橋君は最初オフィスから出発する
    # 3.訪問したレストランが50軒に達するまで、今いる場所から一番近いレストランに移動することを繰り返す
    # 4.受けた注文を捌ききるまで、今いる場所から一番近い配達先に移動することを繰り返す
    # 5.オフィスに帰る
    
    #orders = []     # 注文の集合
    route = []      # 配達ルート
    candidate = [] #真の注文の候補（50個）
    restaurant_dict = {}
    destination_dict = {}
    start_time = time.time()
    
    
    candidate = list(select_orders)
    orders = list(select_orders)
    # 2.オフィスからスタート
    route.append(input_data.office)
    current_position = input_data.office # 現在地
    total_dist = 0                       # 総移動距離
    
    # 3.訪問したレストランが50軒に達するまで、今いる場所から一番近いレストランに移動することを繰り返す
    
    # 同じレストランを2回訪れてはいけないので、訪問済みのレストランを記録する
    #visited_restaurant = [False for _ in range(input_data.order_count)]
    visited_restaurant = {cand: False for cand in candidate}
    
    #行ける座標リスト
    #pos_candidate = [input_data.restaurants[i] for i in true_candidate]

    # pickup_count(=50)回ループ
    for i in range(len(orders)*2):
        # レストランを全探索して、最も近いレストランを探す
        nearest_cand = 0 # レストランの番号
        min_dist = 1000000     # 最も近いレストランの距離
        
        # 候補にした注文だけを調べる
        for j in candidate:
            if visited_restaurant[j]:
                distance = current_position.dist(input_data.destinations[j])
            else:
                distance = current_position.dist(input_data.restaurants[j])            
            if distance < min_dist:
                min_dist = distance
                nearest_cand = j
        
        # 最も近いレストラン(nearest_restaurant)に移動する
        # 現在位置を最も近いレストランの位置に更新
        if visited_restaurant[nearest_cand]:
            current_position = input_data.destinations[nearest_cand]
            candidate.remove(nearest_cand)
            destination_dict[nearest_cand] = i+1
        else:
            current_position = input_data.restaurants[nearest_cand]
            visited_restaurant[nearest_cand] = True
            restaurant_dict[nearest_cand] = i+1
        #current_position = input_data.restaurants[nearest_restaurant]
        
        
        # 配達ルートに現在の位置を追加
        route.append(current_position)
        
        
        # 総移動距離の更新
        total_dist += min_dist
        
        # デバッグしやすいよう、標準エラー出力にレストランを出力
        # 標準エラー出力はデバッグに有効なので、AHCでは積極的に活用していきましょう
        #restaurant_pos = input_data.restaurants[nearest_restaurant]
        #print(f"{i}番目のレストラン: p_{nearest_restaurant} = ({restaurant_pos.x}, {restaurant_pos.y})", file=sys.stderr)
                
    # 5.オフィスに戻る
    route.append(input_data.office)
    total_dist += current_position.dist(input_data.office)
    
    # 合計距離を標準エラー出力に出力
    print("total distance:", total_dist, file=sys.stderr)
    finish_time = time.time()
    
    return Output(orders, route, destination_dict, restaurant_dict, finish_time-start_time)

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

def solve_reduce(input_data: Input, select_orders: list[int]) -> Output:
    start_time = time.time()
    selected_order = list(select_orders)
    output_data_greedy = solve_greedy(input_data, selected_order)
    output_data_greedy.print_output()
    route = list(output_data_greedy.route)
    destination_dict = dict(output_data_greedy.destination_dict)
    restaurant_dict = dict(output_data_greedy.restaurant_dict)
    selected_order = list(output_data_greedy.orders)
    for i in range(len(selected_order)-input_data.pickup_count):
        delta_route_length = [0]*1000
        max_delta = 0
        max_delta_order = 0
        for j in selected_order:
            if destination_dict[j] - restaurant_dict[j] == 1:#レストランと配達先の巡回順が隣り合っているか
                delta_route_length[j] = route[restaurant_dict[j]].dist(route[destination_dict[j]])+route[restaurant_dict[j]].dist(route[restaurant_dict[j]-1])+route[destination_dict[j]].dist(route[destination_dict[j]+1])-route[restaurant_dict[j]-1].dist(route[destination_dict[j]+1])
            else:
                delta_route_length[j] = route[restaurant_dict[j]].dist(route[restaurant_dict[j]+1])+route[restaurant_dict[j]].dist(route[restaurant_dict[j]-1])-route[restaurant_dict[j]-1].dist(route[restaurant_dict[j]+1])+route[destination_dict[j]].dist(route[destination_dict[j]+1])+route[destination_dict[j]].dist(route[destination_dict[j]-1])-route[destination_dict[j]+1].dist(route[destination_dict[j]-1])
            if delta_route_length[j] >= max_delta:
                max_delta_order = j
                max_delta = delta_route_length[j]
        #削除するインデックスを保存
        restaurant_index = restaurant_dict[max_delta_order]
        destination_index = destination_dict[max_delta_order]
        selected_order.remove(max_delta_order)
        #routeの削除
        #route.pop(destination_dict[max_delta_order])
        #route.pop(restaurant_dict[max_delta_order])
        #dictの更新
        for key in restaurant_dict:
            if restaurant_dict[key] >= destination_index:
                restaurant_dict[key] -= 1
            if restaurant_dict[key] >= restaurant_index:
                restaurant_dict[key] -= 1
        for key in destination_dict:
            if destination_dict[key] >= destination_index:
                destination_dict[key] -= 1
            if destination_dict[key] >= restaurant_index:
                destination_dict[key] -= 1
        del destination_dict[max_delta_order]
        del restaurant_dict[max_delta_order]
        print(f"Before delete {max_delta_order}: route =", file=sys.stderr)
        for p in route:
            print(f" {p.x} {p.y}", end="",file=sys.stderr)
        print("",file=sys.stderr)
        route.pop(destination_index)
        route.pop(restaurant_index)
        print(f"After delete {max_delta_order}: route =", file=sys.stderr)
        for p in route:
            print(f" {p.x} {p.y}", end="",file=sys.stderr)
        print("",file=sys.stderr)
        progress_output = Output(selected_order,route,destination_dict,restaurant_dict,time.time()-start_time)
        print(f"delete_order: {max_delta_order}",file=sys.stderr)
        #progress_output.print_output()

    finish_time = time.time()
    return Output(selected_order,route,destination_dict,restaurant_dict,finish_time-start_time)


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
    destination_dict = dict(output_data_greedy.destination_dict)
    restaurant_dict = dict(output_data_greedy.restaurant_dict)
    reduce_time = float(output_data_greedy.time)
    
    # 現在の経路の距離を計算
    current_dist = get_distance(route)
    
    # 乱数生成器のシード値を設定
    # 乱数のシード値は固定のものにしておくと、デバッグがしやすくなります
    random.seed(42)
    
    # 焼きなまし法の開始時刻を取得
    start_time = time.time()
    
    # 制限時間(1.7秒)
    # 2秒ちょうどまでやるとTLEになるので、1.9秒(pypy3で提出する場合は1.7秒)程度にしておくとよい
    time_limit = 1.9-reduce_time
    
    # 開始温度と終了温度
    start_temperature = 2e2
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
        # 訪問先が配達先であるようなインデックスの中から、
        # 「i番目の訪問先をj番目に移動」する操作をランダムに選ぶことで、
        # ある配達先を訪れる順序を他の配達先の間に変える
        # 貪欲法で求めた解では、配達先の訪問順序は0-indexedで51番目～100番目であることに注意
        # (AtCoderオフィス、レストラン50軒、配達先50軒、AtCoderオフィスの順に並んでいる)
            
        # 試行回数のカウントを増やす
        # 進行状況を可視化するため、一定回数ごとに現在の試行回数と合計距離を標準エラー出力に出力
        iteration += 1
        if iteration % 100000 == 0:
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
    print("total distance:", current_dist, file=sys.stderr)
    
    return Output(orders, route, destination_dict, restaurant_dict, time.time()-start_time)


def main():
    # 入力データを受け取る
    global global_start
    global_start = time.time()
    input_data = Input.read()
    orders = [int(x) for x in range(input_data.order_count)]
    selected_order = []
    #周囲350マス以内のものに絞る
    for i in orders:
        if 350 >= max(input_data.office.dist(input_data.restaurants[i]),input_data.office.dist(input_data.destinations[i])):
            selected_order.append(i)
    #print(len(selected_order))
    output_reduce = solve_reduce(input_data,selected_order)
    #output_sa = solve_simulated_annealing(input_data,output_reduce)
    output_reduce.print_output()
    

if __name__ == "__main__":
    main()