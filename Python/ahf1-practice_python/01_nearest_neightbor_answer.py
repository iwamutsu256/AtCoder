"""
01_nearest_neighbor_answer.py

今いる点から最も近いレストランに行くことを50回繰り返し、その後今いる点から最も近い目的地に行くことを50回繰り返す解法プログラム
"""

import sys
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

def solve(input_data: Input) -> Output:
    """
    問題を解く関数（この関数を実装していきます）
    
    Args:
        input_data (Input): 入力データ
        
    Returns:
        Output: 出力データ
    """
    # 貪欲その1
    # 以下を順に実行するプログラム
    # 1.高橋君は最初オフィスから出発する
    # 2.訪問したレストランが50軒に達するまで、今いる場所から一番近いレストランに移動することを繰り返す
    # 3.受けた注文を捌ききるまで、今いる場所から一番近い配達先に移動することを繰り返す
    # 4.オフィスに帰る
    
    orders = [] # 注文の集合
    route = []  # 配達ルート
    
    # 1.オフィスからスタート
    route.append(input_data.office)
    current_position = input_data.office # 現在地
    total_dist = 0                       # 総移動距離
    
    # 2.訪問したレストランが50軒に達するまで、今いる場所から一番近いレストランに移動することを繰り返す
    
    # 同じレストランを2回訪れてはいけないので、訪問済みのレストランを記録する
    visited_restaurant = [False for _ in range(input_data.order_count)]
    
    # pickup_count(=50)回ループ
    for i in range(input_data.pickup_count):
        # レストランを全探索して、最も近いレストランを探す
        nearest_restaurant = 0 # レストランの番号
        min_dist = 1000000     # 最も近いレストランの距離
        
        for j in range(input_data.order_count):
            # 【穴埋め】既に訪れていたらスキップ
            if visited_restaurant[j]:
                continue
            
            # 【穴埋め】最短距離が更新されたら記録
            # 【ヒント】distance = p0.dist(p1) と書くと、p0とp1のマンハッタン距離が計算できる
            # 【ヒント】nearest_restaurant, min_distの2つを更新する
            distance = current_position.dist(input_data.restaurants[j])
            
            if distance < min_dist:
                min_dist = distance
                nearest_restaurant = j
        
        # 最も近いレストラン(nearest_restaurant)に移動する
        # 【穴埋め】現在位置を最も近いレストランの位置に更新
        current_position = input_data.restaurants[nearest_restaurant]
        
        # 【穴埋め】注文の集合に選んだレストランを追加
        orders.append(nearest_restaurant)
        
        # 【穴埋め】配達ルートに現在の位置を追加
        route.append(current_position)
        
        # 【穴埋め】訪問済みレストランの配列にTrueをセット
        visited_restaurant[nearest_restaurant] = True
        
        # 総移動距離の更新
        total_dist += min_dist
        
        # デバッグしやすいよう、標準エラー出力にレストランを出力
        # 標準エラー出力はデバッグに有効なので、AHCでは積極的に活用していきましょう
        restaurant_pos = input_data.restaurants[nearest_restaurant]
        print(f"{i}番目のレストラン: p_{nearest_restaurant} = ({restaurant_pos.x}, {restaurant_pos.y})", file=sys.stderr)
        
    # 【ヒント】ここまで穴埋めできたら、正しく動くか一度実行してみましょう！
    
    # 3.受けた注文を捌ききるまで、今いる場所から一番近い配達先に移動することを繰り返す
    
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
            # 【穴埋め】最短距離が更新されたら記録
            # 【ヒント】nearest_index, nearest_destination, min_distの3つを更新する
            distance = current_position.dist(input_data.destinations[destinations[j]])
            
            if distance < min_dist:
                min_dist = distance
                nearest_index = j
                nearest_destination = destinations[j]
        
        # 最も近い配達先(nearest_destination)に移動する
        # 【穴埋め】現在位置を最も近い配達先の位置に更新
        current_position = input_data.destinations[nearest_destination]
        
        # 【穴埋め】配達ルートに現在の位置を追加
        route.append(current_position)
        
        # 【穴埋め】配達先のリストから削除
        destinations.pop(nearest_index)
        
        # 総移動距離の更新
        total_dist += min_dist
        
        # デバッグしやすいよう、標準エラー出力に配達先を出力
        destination_pos = input_data.destinations[nearest_destination]
        print(f"{i}番目の配達先: q_{nearest_destination} = ({destination_pos.x}, {destination_pos.y})", file=sys.stderr)
        
    # 4.オフィスに戻る
    route.append(input_data.office)
    total_dist += current_position.dist(input_data.office)
    
    # 合計距離を標準エラー出力に出力
    print("total distance:", total_dist, file=sys.stderr)
    
    return Output(orders, route)

def main():
    # 入力データを受け取る
    input_data = Input.read()
    
    # 問題を解く
    output_data = solve(input_data)
    
    # 出力する
    output_data.print_output()

if __name__ == "__main__":
    main()