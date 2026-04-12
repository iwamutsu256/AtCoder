import sys
import math
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Point:
    """
    2次元座標上の点を表すクラス
    """
    x: int
    y: int

    def dist(self, p:'Point') -> int:
        """
        2点間の距離を計算する
        
        Args:
            p (Point):距離を計算する点

        Returns:
            int: 2点間の距離
        """
        delta_x = self.x - p.x
        delta_y = self.y - p.y
        dist = math.sqrt(delta_x**2+delta_y**2)
        return math.floor(dist)

@dataclass
class City:
    """
    都市を表すクラス
    
    Attributes:
        left_up (Point): 都市が存在する可能性がある長方形の左上の座標
        right_down (Point): 都市が存在する可能性がある長方形の右下の座標
        predicted_pos (Point): 都市の予測座標
        idx (int): 都市の名前(0-indexed)
    """
    left_up : Point
    right_down : Point
    idx : int
    predicted_pos: Point

    def __init__(self, left_up: Point, right_down: Point, idx: int):
        """
        都市の予測座標を長方形の中心に設定する
        
        Args:
            left_up (Point): 都市が存在する可能性がある長方形の左上の座標
            right_down (Point): 都市が存在する可能性がある長方形の右下の座標
        """
        self.left_up = left_up
        self.right_down = right_down
        self.idx = int(idx)

        center_x = (left_up.x+right_down.x)//2
        center_y = (left_up.y+right_down.y)//2
        
        self.predicted_pos = Point(center_x,center_y)

@dataclass
class Edge:
    """
    2次元座標上の辺を表すクラス
    
    Attributes:
        a (City): 始点の都市
        b (City): 終点の都市
    """
    a: City
    b: City

    def predicted_length(self) -> int:
        """
        辺の予測される長さを計算する
        
        Returns:
            int: 辺の長さ
        """
        return self.a.predicted_pos.dist(self.b.predicted_pos)

@dataclass
class Group:
    """
    グループを表すクラス
    
    Attributes:
        cities (list[City]): グループに含まれる都市
        edges (list[Edge]): 都市間を結ぶ道路の組
        idx (int): グループの名前(0-indexed)
    """
    cities: list = field(default_factory = list)
    edges: list = field(default_factory = list)
    idx: int = 0

@dataclass
class Input:
    """
    入力データを表すクラス
    
    Attributes:
        cities_count (int): 都市の個数 (=800)
        group_count (int): 回答における都市のグループの個数
        max_query_count (int): 最大クエリ回数
        query_max_cities_size (int): クエリを行う都市の集合のサイズの上限
        max_rect_size (int): 都市が含まれる長方形の幅や高さとしてありうる最大値
        group_cities_count (list[int]): 各グループに割り当てる都市の個数を表す配列
        cities (list[City]): 都市の配列
    """
    cities_count: int
    group_count: int
    max_query_count: int
    query_max_cities_size: int
    max_rect_size: int
    group_cities_count: list[int]
    cities: list[City]

    @staticmethod
    def read() -> 'Input':
        """
        入力データを読み込む
        
        Returns:
            Input: 読み込んだ入力データ
        """
        cities_count, group_count, max_query_count, query_max_cities_size, max_rect_size = map(int,input().split())
        group_cities_count = list(map(int,input().split()))
        cities = []
        for i in range(cities_count):
            l_x, r_x, l_y, r_y = map(int,input().split())
            cities.append(City(Point(l_x,l_y),Point(r_x,r_y),i))
        
        return Input(cities_count,group_count, max_query_count, query_max_cities_size, max_rect_size, group_cities_count, cities)

@dataclass
class Output:
    """
    出力データを表すクラス
    
    Attributes:
        group_list (list[Group]): グループのリスト
    """
    group_list: list[Group]

    def print_output(self):
        """
        解を出力する
        """
        print("!")
        #分割したすべてのグループに対して行う
        for group in self.group_list:
            #グループ内の都市を出力
            if group.cities:
                print(" ".join(str(city.idx) for city in group.cities))

            #すべての辺を出力
            for edge in group.edges:
                print(edge.a.idx,edge.b.idx)
        
        print()

class UnionFind():
    """
    Union Find木クラス

    Attributes
    --------------------
    n : int
        要素数
    root : list
        木の要素数
        0未満であればそのノードが根であり、添字の値が要素数
    rank : list
        木の深さ
    """

    def __init__(self, n):
        """
        Parameters
        ---------------------
        n : int
            要素数
        """
        self.n = n
        self.root = [-1]*(n+1)
        self.rank = [0]*(n+1)

    def find(self, x):
        """
        ノードxの根を見つける

        Parameters
        ---------------------
        x : int
            見つけるノード

        Returns
        ---------------------
        root : int
            根のノード
        """
        if(self.root[x] < 0):
            return x
        else:
            self.root[x] = self.find(self.root[x])
            return self.root[x]

    def unite(self, x, y):
        """
        木の併合

        Parameters
        ---------------------
        x : int
            併合したノード
        y : int
            併合したノード
        """
        x = self.find(x)
        y = self.find(y)

        if(x == y):
            return
        elif(self.rank[x] > self.rank[y]):
            self.root[x] += self.root[y]
            self.root[y] = x
        else:
            self.root[y] += self.root[x]
            self.root[x] = y
            if(self.rank[x] == self.rank[y]):
                self.rank[y] += 1

    def same(self, x, y):
        """
        同じグループに属するか判定

        Parameters
        ---------------------
        x : int
            判定したノード
        y : int
            判定したノード

        Returns
        ---------------------
        ans : bool
            同じグループに属しているか
        """
        return self.find(x) == self.find(y)

    def size(self, x):
        """
        木のサイズを計算

        Parameters
        ---------------------
        x : int
            計算したい木のノード

        Returns
        ---------------------
        size : int
            木のサイズ
        """
        return -self.root[self.find(x)]

    def roots(self):
        """
        根のノードを取得

        Returns
        ---------------------
        roots : list
            根のノード
        """
        return [i for i, x in enumerate(self.root) if x < 0]

    def group_size(self):
        """
        グループ数を取得

        Returns
        ---------------------
        size : int
            グループ数
        """
        return len(self.roots())

    def group_members(self):
        """
        全てのグループごとのノードを取得

        Returns
        ---------------------
        group_members : defaultdict
            根をキーとしたノードのリスト
        """
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

def solve(input_data: Input) -> Output:
    """
    問題を解く関数
    
    Args:
        input_data (Input): 入力データ
    
    Returns:
        Output: 出力データ
    """
    #解法2
    # 候補の中で一番左のものをとり、グループに入れる
    # そこから近い順にグループ内の都市の数だけ取る。
    # これを繰り返してグループ分けをする
    # グループ内の都市についてクラスカル法でつなぐ
    group_list = [] #groupの配列

    cities = input_data.cities
    #ソートした都市の配列を候補として使う
    sorted_cities = sorted(input_data.cities, key=lambda city: (city.predicted_pos.x, city.predicted_pos.y))

    for i in range(input_data.group_count):
        # グループを作成
        group = Group([],[],i)
        g_c_count = input_data.group_cities_count[i]
        # 先頭の要素を現在位置に設定
        current_pos = sorted_cities[0].predicted_pos
        group.cities.append(sorted_cities[0])
        # 候補から外す
        sorted_cities.pop(0)
        # 現在位置から近いものをsorted_citiesからg_c_count-1個選ぶ
        # 選んだものはsorted_citiesから削除する
        sorted_by_distance = sorted(sorted_cities, key=lambda city: current_pos.dist(city.predicted_pos))
        # 選んだものをグループに追加し、sorted_citiesから削除
        for j in range(g_c_count-1):
            group.cities.append(sorted_by_distance[j])
            sorted_cities.remove(sorted_by_distance[j])
        
        # インデックスのマッピングを作成
        local_index_map = {city.idx: idx for idx, city in enumerate(group.cities)}
        revevrse_index_map = {idx: city.idx for idx, city in enumerate(group.cities)}

        # グループ内の都市について最小全域木を作成する
        uf = UnionFind(g_c_count)
        edges = []
        for k in group.cities:
            for l in group.cities:
                if k.idx < l.idx:
                    predicted_distance = k.predicted_pos.dist(l.predicted_pos)
                    edges.append((predicted_distance, local_index_map[k.idx], local_index_map[l.idx]))
        edges.sort()
        for edge in edges:
            predicted_distance, node1, node2 = edge
            if not uf.same(node1,node2):
                uf.unite(node1, node2)
                group.edges.append(Edge(cities[revevrse_index_map[node1]], cities[revevrse_index_map[node2]]))
        group_list.append(group)

    return Output(group_list)

def main():
    # 入力データを受け取る
    input_data = Input.read()

    #問題を解く
    output_data = solve(input_data)#未実装

    # 出力する
    output_data.print_output()

if __name__ == "__main__":
    main()