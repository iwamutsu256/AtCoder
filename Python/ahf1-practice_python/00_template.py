"""
00_template.py

AtCoder Heuristic First-step Vol.1のPython向けテンプレートファイル
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
    # サンプル解法
    # 以下を順に実行するプログラム
    # 1.高橋君は最初オフィスから出発する
    # 2.0番目のレストラン, 0番目の配達先, ..., 49番目のレストラン, 49番目の配達先の順に移動する
    # 3.オフィスに帰る
    
    orders = [] # 注文の集合
    route = []  # 配達ルート
    
    # 1.オフィスからスタート
    route.append(input_data.office)
    current_position = input_data.office # 現在地
    total_dist = 0                       # 総移動距離
    
    # 2.レストランと配達先を50箇所（pickup_count）ずつ巡る
    for i in range(input_data.pickup_count):
        # 次のレストランに移動する
        # 注文の集合にi番目のレストランを追加
        orders.append(i)

        # 配達ルートにi番目のレストランの位置を追加
        route.append(input_data.restaurants[i])

        # 総移動距離の更新
        total_dist += current_position.dist(input_data.restaurants[i])

        # 現在位置をi番目のレストランの位置に更新
        current_position = input_data.restaurants[i]

        # 次の配達先に移動する
        # 配達ルートにi番目の配達先の位置を追加
        route.append(input_data.destinations[i])

        # 総移動距離の更新
        total_dist += current_position.dist(input_data.destinations[i])

        # 現在位置を最も近い配達先の位置に更新
        current_position = input_data.destinations[i]
        
    # 3.オフィスに戻る
    route.append(input_data.office)
    total_dist += current_position.dist(input_data.office)
    
    # 合計距離を標準エラー出力に出力
    # 標準エラー出力はデバッグに有効なので、AHCでは積極的に活用していきましょう
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