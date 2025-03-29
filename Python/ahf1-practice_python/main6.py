"""
すべてのレストランと配達先を通る貪欲ルートから一番減少幅が大きい注文番号を繰り返し消していく
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



def main():
    # 入力データを受け取る
    global global_start
    global_start = time.time()
    input_data = Input.read()
    orders = [int(x) for x in range(input_data.order_count)]
    for i in range(950):
        output_data_greedy = solve_greedy(input_data, orders)
        # # 出力する
        output_data_greedy.print_output()
        route = list(output_data_greedy.route)
        destination_dict = dict(output_data_greedy.destination_dict)
        restaurant_dict = dict(output_data_greedy.restaurant_dict)
        orders = list(output_data_greedy.orders)
        delta_route_length = [0]*1000
        max_delta = 0
        max_delta_order = 0
        for j in orders:
            if destination_dict[j] - restaurant_dict[j] == 1:
                delta_route_length[j] = route[restaurant_dict[j]].dist(route[destination_dict[j]])+route[restaurant_dict[j]].dist(route[restaurant_dict[j]-1])+route[destination_dict[j]].dist(route[destination_dict[j]+1])-route[restaurant_dict[j]-1].dist(route[destination_dict[j]+1])
            else:
                delta_route_length[j] = route[restaurant_dict[j]].dist(route[restaurant_dict[j]+1])+route[restaurant_dict[j]].dist(route[restaurant_dict[j]-1])-route[restaurant_dict[j]-1].dist(route[restaurant_dict[j]+1])+route[destination_dict[j]].dist(route[destination_dict[j]+1])+route[destination_dict[j]].dist(route[destination_dict[j]-1])-route[destination_dict[j]+1].dist(route[destination_dict[j]-1])
            if delta_route_length[j] >= max_delta:
                max_delta_order = j
                max_delta = delta_route_length[j]
        orders.remove(max_delta_order)
    solve_greedy(input_data, orders).print_output

if __name__ == "__main__":
    main()