"""
03_simulated_annealing.py

貪欲法で初期解を求めた後、配達先の訪問順序を焼きなまし法で改善する解法プログラム
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

def solve_greedy(input_data: Input) -> Output:
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
    
    candidates = [] # 注文の候補
    orders = []     # 注文の集合
    route = []      # 配達ルート
    
    # 1.オフィスから距離400以下の注文だけを候補にする
    for i in range(input_data.order_count):
        if input_data.office.dist(input_data.restaurants[i]) <= 400 and input_data.office.dist(input_data.destinations[i]) <= 400:
            candidates.append(i)
    
    # 2.オフィスからスタート
    route.append(input_data.office)
    current_position = input_data.office # 現在地
    total_dist = 0                       # 総移動距離
    
    # 3.訪問したレストランが50軒に達するまで、今いる場所から一番近いレストランに移動することを繰り返す
    
    # 同じレストランを2回訪れてはいけないので、訪問済みのレストランを記録する
    visited_restaurant = [False for _ in range(input_data.order_count)]
    
    # pickup_count(=50)回ループ
    for i in range(input_data.pickup_count):
        # レストランを全探索して、最も近いレストランを探す
        nearest_restaurant = 0 # レストランの番号
        min_dist = 1000000     # 最も近いレストランの距離
        
        # 候補にした注文だけを調べる
        for j in candidates:
            # 既に訪れていたらスキップ
            if visited_restaurant[j]:
                continue
            
            # 最短距離が更新されたら記録
            distance = current_position.dist(input_data.restaurants[j])
            
            if distance < min_dist:
                min_dist = distance
                nearest_restaurant = j
        
        # 最も近いレストラン(nearest_restaurant)に移動する
        # 現在位置を最も近いレストランの位置に更新
        current_position = input_data.restaurants[nearest_restaurant]
        
        # 注文の集合に選んだレストランを追加
        orders.append(nearest_restaurant)
        
        # 配達ルートに現在の位置を追加
        route.append(current_position)
        
        # 【穴埋め】訪問済みレストランの配列にTrueをセット
        visited_restaurant[nearest_restaurant] = True
        
        # 総移動距離の更新
        total_dist += min_dist
        
        # デバッグしやすいよう、標準エラー出力にレストランを出力
        # 標準エラー出力はデバッグに有効なので、AHCでは積極的に活用していきましょう
        restaurant_pos = input_data.restaurants[nearest_restaurant]
        print(f"{i}番目のレストラン: p_{nearest_restaurant} = ({restaurant_pos.x}, {restaurant_pos.y})", file=sys.stderr)
        
    # 4.受けた注文を捌ききるまで、今いる場所から一番近い配達先に移動することを繰り返す
    
    # 行かなければいけない配達先のリスト
    # ordersは最終的に出力しなければならないので、ここでコピーを作成しておく
    # 配達先を訪問したらこのリストから1つずつ削除していく
    destinations = list(orders)
    
    # pickup_count(=50)回ループ
    for i in range(input_data.pickup_count):
        # 配達先を全探索して、最も近い配達先を探す
        nearest_index = 0                                 # 配達先リストのインデックス
        nearest_destination = destinations[nearest_index] # 配達先の番号
        min_dist = 1000000                                # 最も近い配達先の距離
        
        # 0～999まで全探索するのではなく、50個のレストランに対応した配達先を全探索することに注意
        for j in range(len(destinations)):
            # 最短距離が更新されたら記録
            distance = current_position.dist(input_data.destinations[destinations[j]])
            
            if distance < min_dist:
                min_dist = distance
                nearest_index = j
                nearest_destination = destinations[j]
        
        # 最も近い配達先(nearest_destination)に移動する
        # 現在位置を最も近い配達先の位置に更新
        current_position = input_data.destinations[nearest_destination]
        
        # 配達ルートに現在の位置を追加
        route.append(current_position)
        
        # 配達先のリストから削除
        destinations.pop(nearest_index)
        
        # 総移動距離の更新
        total_dist += min_dist
        
        # デバッグしやすいよう、標準エラー出力に配達先を出力
        destination_pos = input_data.destinations[nearest_destination]
        print(f"{i}番目の配達先: q_{nearest_destination} = ({destination_pos.x}, {destination_pos.y})", file=sys.stderr)
        
    # 5.オフィスに戻る
    route.append(input_data.office)
    total_dist += current_position.dist(input_data.office)
    
    # 合計距離を標準エラー出力に出力
    print("total distance:", total_dist, file=sys.stderr)
    
    return Output(orders, route)

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
    
    # 現在の経路の距離を計算
    current_dist = get_distance(route)
    
    # 乱数生成器のシード値を設定
    # 乱数のシード値は固定のものにしておくと、デバッグがしやすくなります
    random.seed(42)
    
    # 焼きなまし法の開始時刻を取得
    start_time = time.time()
    
    # 制限時間(1.7秒)
    # 2秒ちょうどまでやるとTLEになるので、1.9秒(pypy3で提出する場合は1.7秒)程度にしておくとよい
    time_limit = 1.7
    
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
        
        # 訪問先が配達先であるようなインデックスの中から、
        # 「i番目の訪問先をj番目に移動」する操作をランダムに選ぶことで、
        # ある配達先を訪れる順序を他の配達先の間に変える
        # 貪欲法で求めた解では、配達先の訪問順序は0-indexedで51番目～100番目であることに注意
        # (AtCoderオフィス、レストラン50軒、配達先50軒、AtCoderオフィスの順に並んでいる)
        
        # 訪問先が配達先であるようなインデックスの中から i, j をランダムに選ぶ
        i = random.randint(0, input_data.pickup_count - 1) + input_data.pickup_count + 1
        j = random.randint(0, input_data.pickup_count - 1) + input_data.pickup_count + 1
        
        # i番目の訪問先をj番目に移動する操作を行う
        point_to_move = route.pop(i)
        route.insert(j, point_to_move)
        
        # 操作後の経路の距離を計算
        new_dist = get_distance(route)
        
        # 【穴埋め】操作後の距離が操作前以下なら採用する
        # 【穴埋め】操作前より悪化していても、確率で採用する(悪化度合いが小さく、温度が高いほど採用されやすい)
        # 【ヒント】採用確率(0.0以上1.0未満)は math.exp((current_dist - new_dist) / current_temperature) で計算できる
        # 【ヒント】random.random() と書くと、0.0以上1.0未満の乱数が得られる
        if current_dist >= new_dist: ## put your code here ##
            current_dist = new_dist
        else:
            if random.random() < math.exp((current_dist - new_dist) / current_temperature):
                current_dist = new_dist
            else:
            # 採用されなかったら元に戻す
                route.pop(j)
                route.insert(i, point_to_move)
            
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
    
    return Output(orders, route)

def main():
    # 入力データを受け取る
    input_data = Input.read()
    
    # 問題を解く
    output_data_greedy = solve_greedy(input_data)
    output_data = solve_simulated_annealing(input_data, output_data_greedy)
    
    # 出力する
    output_data.print_output()

if __name__ == "__main__":
    main()