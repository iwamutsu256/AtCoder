import sys
import math
import random
import time
import heapq
from dataclasses import dataclass, field
from collections import defaultdict,deque
from scipy.spatial import Delaunay

global_start_time = time.time()

@dataclass
class Point:
    """
    2次元座標上の点を表すクラス
    """
    x: float
    y: float

    def dist(self, p:'Point') -> float:
        """
        2点間の距離を計算する
        
        Args:
            p (Point):距離を計算する点

        Returns:
            float: 2点間の距離
        """
        delta_x = self.x - p.x
        delta_y = self.y - p.y
        dist = math.sqrt(delta_x**2+delta_y**2)
        return dist
    
    def plus(self, p:'Point') -> 'Point':
        """
        2点の座標の足し算
        
        Args:
            p (Point): 足す座標
        
        Returns:
            Point: 足し算の結果の座標
        """
        return Point(self.x+p.x,self.y+p.y)
    
    def times(self, n: float) -> 'Point':
        """
        点の座標の定数倍
        
        Args:
            n (float): かける定数
            
        Returns:
            Point: 結果の座標
        """
        return Point(self.x*n,self.y*n)
    
    def divide(self, n: float) -> 'Point':
        """点の座標の定数分の１倍
        
        Args:
            n (float): 割る定数
        
        Returns:
            Point: 結果の座標
        """
        return self.times(1/n)

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

        center_x = (left_up.x+right_down.x)/2
        center_y = (left_up.y+right_down.y)/2
        
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

    def predicted_length(self) -> float:
        """
        辺の予測される長さを計算する
        
        Returns:
            float: 辺の長さ
        """
        return self.a.predicted_pos.dist(self.b.predicted_pos)

class Group:
    """
    グループを表すクラス
    
    Attributes:
        cities (list[City]): グループに含まれる都市
        edges (list[Edge]): 都市間を結ぶ道路の組
        idx (int): グループの名前(0-indexed)
        center_of_gravity (Point): 重心の座標
        score (float): スコア
    """
    def __init__(self,idx: int):
        self.cities = []
        self.edges = []
        self.center_of_gravity = Point(0,0)
        self.idx = int(idx)
        self.score = float(0.0) 

    def add_city(self,city: City):
        """
        グループに都市を追加し、重心を更新する
        
        Returns:
            Point: 重心
        """
        if len(self.cities) == 0:
            # 追加した点が一つ目なら、それが重心となる
            self.center_of_gravity = city.predicted_pos
        else:
            # 追加した点が二つ目以降なら、重心を計算しなおす
            # すべての座標を足したもの
            sum_city_point = self.center_of_gravity.times(len(self.cities)).plus(city.predicted_pos)
            new_center_of_gravity = sum_city_point.divide(len(self.cities)+1)
            self.center_of_gravity = new_center_of_gravity
        self.cities.append(city)
        return self.center_of_gravity

    def remove_city(self, city: City):
        """
        グループから都市を削除する
        
        Returns:
            Point: 重心
        """
        if len(self.cities) == 1:
            # 削除する点がラスト一つなら、重心を(0,0)にリセットする
            self.center_of_gravity = Point(0,0)
        else:
            # 重心を計算しなおす
            sum_city_point = self.center_of_gravity.times(len(self.cities)).plus(city.predicted_pos.times(-1))
            new_center_of_gravity = sum_city_point.divide(len(self.cities)-1)
            self.center_of_gravity = new_center_of_gravity
        self.cities.remove(city)
        return self.center_of_gravity

    def calculate_score(self) -> float:
        """
        グループの重心から都市の距離の総和を計算する

        Returns:
            float: スコア
        """
        if len(self.cities) <= 1:
            self.score = 0.0
            return self.score
        else:
            score = 0
            for city in self.cities:
                distance = city.predicted_pos.dist(self.center_of_gravity)
                score += distance
            self.score = score
        return self.score

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

def forecast(query_cities: list[City]) -> list[Edge]:
    """
    占いをする関数
    
    Args:
        query_cities (list[City]): 占いをする都市の配列
    
    Returns:
        edges (list[Edge]): 占い結果の辺の配列
    """
    edges = []
    # 都市のインデックスと都市のインスタンスの辞書を作成
    cities_dict = {}
    for city in query_cities:
        key = city.idx
        cities_dict[key] = city
    # 占いは二つ以上の都市について行われる
    if len(query_cities) < 2:
        pass
    else:
        # クエリの文字列を作成
        query = []
        query.append("?")
        query.append(str(len(query_cities)))
        # リストから都市のインデックスを取得
        for i in range(len(query_cities)):
            query.append(str(query_cities[i].idx))
        # 質問
        print(" ".join(query), flush=True)
        # N個の都市に対してN-1個の辺が返ってくる
        for i in range(len(query_cities)-1):
            idx_a,idx_b = map(int,input().split())
            a = cities_dict[idx_a]
            b = cities_dict[idx_b]
            edges.append(Edge(a,b))
    return edges

def point_shrink(edge: Edge):
    """
    辺の長さを短くするように両端の都市の予想座標をランダム変化させる
    
    Args:
        edge (Edge): 変化させる辺

    Returns:
        None
    """
    # 始点と終点の都市を取得
    city_a = edge.a
    city_b = edge.b
    # それぞれの予測座標から位置関係を分類
    # 都市Bに対して都市Aがどの位置にあるか
    # 左上
    if city_a.predicted_pos.x <= city_b.predicted_pos.x and city_a.predicted_pos.y <= city_b.predicted_pos.y:
        # 都市Aを右下、都市Bを左上にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.predicted_pos.x,city_a.right_down.x)
        city_a.predicted_pos.y = random.uniform(city_a.predicted_pos.y,city_a.right_down.y)
        city_b.predicted_pos.x = random.uniform(city_b.left_up.x,city_b.predicted_pos.x)
        city_b.predicted_pos.y = random.uniform(city_b.left_up.y,city_b.predicted_pos.y)
    # 右上
    elif city_a.predicted_pos.x >= city_b.predicted_pos.x and city_a.predicted_pos.y <= city_b.predicted_pos.y:
        # 都市Aを左下、都市Bを右上にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.left_up.x,city_a.predicted_pos.x)
        city_a.predicted_pos.y = random.uniform(city_a.predicted_pos.y, city_a.right_down.y)
        city_b.predicted_pos.x = random.uniform(city_b.predicted_pos.x, city_b.right_down.x)
        city_b.predicted_pos.y = random.uniform(city_b.left_up.y, city_b.predicted_pos.y)
    # 右下
    elif city_a.predicted_pos.x >= city_b.predicted_pos.x and city_b.predicted_pos.y >= city_b.predicted_pos.y:
        # 都市Aを左上、都市Bを右下にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.left_up.x, city_a.predicted_pos.x)
        city_a.predicted_pos.y = random.uniform(city_a.left_up.y, city_a.predicted_pos.y)
        city_b.predicted_pos.x = random.uniform(city_b.predicted_pos.x, city_b.right_down.x)
        city_b.predicted_pos.y = random.uniform(city_b.predicted_pos.y, city_b.right_down.y)
    # 左下
    else:
        # 都市Aを右上、都市Bを左下にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.predicted_pos.x, city_a.right_down.x)
        city_a.predicted_pos.y = random.uniform(city_a.left_up.y, city_a.predicted_pos.y)
        city_b.predicted_pos.x = random.uniform(city_b.left_up.x, city_b.predicted_pos.x)
        city_b.predicted_pos.y = random.uniform(city_b.predicted_pos.y, city_b.right_down.y)
    return

def point_expand(edge: Edge):
    """
    辺の長さを長くするように両端の都市の予想座標をランダム変化させる
    
    Args:
        edge (Edge): 変化させる辺
    
    Returns:
        None
    """
    # 始点と終点の都市を取得
    city_a = edge.a
    city_b = edge.b
    # それぞれの予測座標から位置関係を分類
    # 都市Bに対して都市Aがどの位置にあるか
    # 左上
    if city_a.predicted_pos.x <= city_b.predicted_pos.x and city_a.predicted_pos.y <= city_b.predicted_pos.y:
        # 都市Aを左上、都市Bを右下にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.left_up.x, city_a.predicted_pos.x)
        city_a.predicted_pos.y = random.uniform(city_a.left_up.y, city_a.predicted_pos.y)
        city_b.predicted_pos.x = random.uniform(city_b.predicted_pos.x, city_b.right_down.x)
        city_b.predicted_pos.y = random.uniform(city_b.predicted_pos.y, city_b.right_down.y)
    # 右上
    elif city_a.predicted_pos.x >= city_b.predicted_pos.x and city_a.predicted_pos.y <= city_b.predicted_pos.y:
        # 都市Aを右上、都市Bを左下にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.predicted_pos.x, city_a.right_down.x)
        city_a.predicted_pos.y = random.uniform(city_a.left_up.y, city_a.predicted_pos.y)
        city_b.predicted_pos.x = random.uniform(city_b.left_up.x, city_b.predicted_pos.x)
        city_b.predicted_pos.y = random.uniform(city_b.predicted_pos.y, city_b.right_down.y)
    # 右下
    elif city_a.predicted_pos.x >= city_b.predicted_pos.x and city_b.predicted_pos.y >= city_b.predicted_pos.y:
        # 都市Aを右下、都市Bを左上にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.predicted_pos.x,city_a.right_down.x)
        city_a.predicted_pos.y = random.uniform(city_a.predicted_pos.y,city_a.right_down.y)
        city_b.predicted_pos.x = random.uniform(city_b.left_up.x,city_b.predicted_pos.x)
        city_b.predicted_pos.y = random.uniform(city_b.left_up.y,city_b.predicted_pos.y)
    # 左下
    else:
        # 都市Aを左下、都市Bを右上にランダムに動かす
        city_a.predicted_pos.x = random.uniform(city_a.left_up.x,city_a.predicted_pos.x)
        city_a.predicted_pos.y = random.uniform(city_a.predicted_pos.y, city_a.right_down.y)
        city_b.predicted_pos.x = random.uniform(city_b.predicted_pos.x, city_b.right_down.x)
        city_b.predicted_pos.y = random.uniform(city_b.left_up.y, city_b.predicted_pos.y)
    return

def cities_move_append(cities_move_vec, i, vec):
    """
    cities_move_vecにベクトルを追加して平均を取り直す関数
    
    Args:
        cities_move_vec (list(tuple(delta_x, delta_y, count))): 各都市の動くべきベクトル
        i (int): 追加するインデックス
        vec (tuple(delta_x, delta_y)): 追加して再計算するタプル
    
    Returns:
        None
    """
    move_vec = cities_move_vec[i]
    # デバッグ用出力
    #print(f"move_vec: {move_vec}",file=sys.stderr, flush = True)
    if move_vec[2] == 0:
        cities_move_vec[i] = (vec[0], vec[1], 1)
    else:
        new_x = (move_vec[0]*move_vec[2]+vec[0])/(move_vec[2]+1)
        new_y = (move_vec[1]*move_vec[2]+vec[1])/(move_vec[2]+1)
        cities_move_vec[i] = (new_x, new_y, move_vec[2]+1)
    return

def count_contradiction(query_ans, cities_move_vec,cities):
    """
    クエリの答えとの矛盾点の数をスコアとして返す関数
    ついでに都市をどの方向に動かすべきかを計算してくれる
    
    Args:
        query_ans (list[list[Edge]]): クエリの返答
        cities_move_vec (list(tuple(delta_x, delta_y, count))): 各都市の動くべきベクトル
    Returns:
        count (int): 矛盾点の数
    """
    count = 0
    # デバッグ用出力
    #print(f"edge0: {query_ans[0]}",file=sys.stderr, flush=True)

    for edges in query_ans:
        for i in range(len(edges) - 1):
            # 短いはずの辺
            short = edges[i]
            # 長いはずの辺
            long = edges[i+1]
            # 理想の大小関係と現実の大小関係が違った場合
            if cities[short.a.idx].predicted_pos.dist(cities[short.b.idx].predicted_pos) > cities[long.a.idx].predicted_pos.dist(cities[long.b.idx].predicted_pos):
                diff = cities[short.a.idx].predicted_pos.dist(cities[short.b.idx].predicted_pos) - cities[long.a.idx].predicted_pos.dist(cities[long.b.idx].predicted_pos)
                count += diff
                # 短い辺は長く、長い辺は短くする
                # 変化の余地を計算し、変化させる割合を決定する
                # 短い辺の変化の余地（現在の辺の長さと最大まで長くしたときの長さの差）
                # 最大まで長くしたときの長さを求める
                # 位置関係aが右下
                if short.a.predicted_pos.x >= short.b.predicted_pos.x and short.a.predicted_pos.y >= short.b.predicted_pos.y:
                    maximum_short = short.a.right_down.dist(short.b.left_up)
                    short_pos_rel = "RD"
                # 位置関係aが右上    
                elif short.a.predicted_pos.x >= short.b.predicted_pos.x and short.a.predicted_pos.y <= short.b.predicted_pos.y:
                    maximum_short = Point(short.a.right_down.x,short.a.left_up.y).dist(Point(short.b.left_up.x, short.b.right_down.y))
                    short_pos_rel = "RU"
                # 位置関係aが左下
                elif short.a.predicted_pos.x <= short.b.predicted_pos.x and short.a.predicted_pos.y >= short.b.predicted_pos.y:
                    maximum_short = Point(short.a.left_up.x, short.a.right_down.y).dist(Point(short.b.right_down.x, short.b.left_up.y))
                    short_pos_rel = "LD"
                # 位置関係aが左上
                else:
                    maximum_short = short.a.left_up.dist(short.b.right_down)
                    short_pos_rel = "LU"
                # 短い辺の変化の余地
                change_short = maximum_short - cities[short.a.idx].predicted_pos.dist(cities[short.b.idx].predicted_pos)
                # 長い辺の変化の余地を調べる
                # 通り越している場合にも対応する
                # 位置関係aが右下
                if long.a.predicted_pos.x >= long.b.predicted_pos.x and long.a.predicted_pos.y >= long.b.predicted_pos.y:
                    minimum_long = math.sqrt((max(0,long.a.left_up.x-long.b.right_down.x))**2 + (max(0,long.a.left_up.y - long.b.right_down.y))**2)
                    long_pos_rel = "RD"
                # 位置関係aが右上    
                elif long.a.predicted_pos.x >= long.b.predicted_pos.x and long.a.predicted_pos.y <= long.b.predicted_pos.y:
                    minimum_long = math.sqrt((max(0,long.a.left_up.x - long.b.right_down.x))**2 + (max(0, long.b.left_up.y - long.a.right_down.y))**2)
                    long_pos_rel = "RU"
                # 位置関係aが左下
                elif long.a.predicted_pos.x <= long.b.predicted_pos.x and long.a.predicted_pos.y >= long.b.predicted_pos.y:
                    minimum_long = math.sqrt((max(0,long.b.left_up.x - long.a.right_down.x))**2 + (max(0, long.a.left_up.y - long.b.right_down.y))**2)
                    long_pos_rel = "LD"
                # 位置関係aが左上
                else:
                    minimum_long = math.sqrt((max(0,long.b.left_up.x - long.a.right_down.x))**2 + (max(0, long.b.left_up.y - long.a.right_down.y))**2)
                    long_pos_rel = "LU"
                change_long = cities[long.a.idx].predicted_pos.dist(cities[long.b.idx].predicted_pos) - minimum_long
                # 短い辺を伸ばす距離
                short_diff = diff*(change_short/(change_short+change_long))
                # デバッグ用出力
                print(f"change_short:{change_short},change_long:{change_long}",file=sys.stderr,flush=True)
                print(f"change_short/(change_short+change_long):{change_short/(change_short+change_long)}",file=sys.stderr,flush=True)
                # 長い辺を縮める距離
                long_diff = diff*(change_long/(change_short+change_long))
                # 短い辺について、両端の都市の移動ベクトルを設定
                # 短い辺のAB方向の単位ベクトル
                vec_short_a_b = ((short.b.predicted_pos.x - short.a.predicted_pos.x)/math.sqrt((short.b.predicted_pos.x - short.a.predicted_pos.x)**2+(short.b.predicted_pos.y - short.a.predicted_pos.y)**2),(short.b.predicted_pos.y - short.a.predicted_pos.y)/math.sqrt((short.b.predicted_pos.x - short.a.predicted_pos.x)**2+(short.b.predicted_pos.y - short.a.predicted_pos.y)**2))
                # デバッグ用出力
                print(f"short 単位ベクトル:{(vec_short_a_b[0],vec_short_a_b[1])},大きさ:{math.sqrt(vec_short_a_b[0]**2+vec_short_a_b[1]**2)}",file=sys.stderr,flush=True)
                if short_pos_rel == "RD":# Aが右下
                    # 一番伸ばした時の角までの距離
                    alpha = short.a.predicted_pos.dist(short.a.right_down)
                    beta = short.b.predicted_pos.dist(short.b.left_up)
                    # 単位ベクトルにかける定数のうち、横の端、縦の端、重みから考える定数の中から一番小さいものを選ぶ
                    # 縦の端（下）
                    if vec_short_a_b[1] != 0:
                        short_a_candidate_1 = (short.a.right_down.y - short.a.predicted_pos.y)/vec_short_a_b[1]
                    else:
                        short_a_candidate_1 = math.inf
                    # 横の端（右）
                    if vec_short_a_b[0] != 0:
                        short_a_candidate_2 = (short.a.right_down.x - short.a.predicted_pos.x)/vec_short_a_b[0]
                    else:
                        short_a_candidate_2 = math.inf
                    # 重みから
                    short_a_candidate_3 = -alpha*short_diff/(alpha+beta)
                    short_a = min(short_a_candidate_1,short_a_candidate_2,short_a_candidate_3)
                    # 短い辺の都市Aに対する移動するべき方向のベクトルを追加
                    cities_move_append(cities_move_vec, short.a.idx, (vec_short_a_b[0]*short_a, vec_short_a_b[1]*short_a))
                    # 縦の端（上）
                    if vec_short_a_b[1] != 0:
                        short_b_candidate_1 = (short.b.left_up.y - short.b.predicted_pos.y)/vec_short_a_b[1]
                    else:
                        short_b_candidate_1 = math.inf
                    # 横の端　(左)
                    if vec_short_a_b[0] != 0:
                        short_b_candidate_2 = (short.b.left_up.x - short.b.predicted_pos.x)/vec_short_a_b[0]
                    else:
                        short_b_candidate_2 = math.inf
                    # 重みから
                    short_b_candidate_3 = beta*short_diff/(alpha+beta)
                    short_b = min(short_b_candidate_1, short_b_candidate_2, short_b_candidate_3)
                    # 短い辺の都市Bに対する移動するべき方向のベクトルを追加
                    cities_move_append(cities_move_vec, short.b.idx, (vec_short_a_b[0]*short_b, vec_short_a_b[1]*short_b))
                elif short_pos_rel == "RU":# Aが右上
                    # 一番伸ばした時の角までの距離
                    alpha = short.a.predicted_pos.dist(Point(short.a.right_down.x, short.a.left_up.y))
                    beta = short.b.predicted_pos.dist(Point(short.b.left_up.x, short.b.right_down.y))
                    # 縦の端（上）
                    if vec_short_a_b[1] != 0:
                        short_a_candidate_1 = (short.a.left_up.y - short.a.predicted_pos.y)/vec_short_a_b[1]
                    else:
                        short_a_candidate_1 = math.inf
                    # 横の端 (右)
                    if vec_short_a_b[0] != 0:
                        short_a_candidate_2 = (short.a.right_down.x - short.a.predicted_pos.x)/vec_short_a_b[0]
                    else:
                        short_a_candidate_2 = math.inf
                    # 重みから
                    short_a_candidate_3 = -alpha*short_diff/(alpha+beta)
                    short_a = min(short_a_candidate_1, short_a_candidate_2, short_a_candidate_3)
                    cities_move_append(cities_move_vec, short.a.idx, (vec_short_a_b[0]*short_a, vec_short_a_b[1]*short_a))
                    # 縦の端（下）
                    if vec_short_a_b[1] != 0:
                        short_b_candidate_1 = (short.b.right_down.y - short.b.predicted_pos.y)/vec_short_a_b[1]
                    else:
                        short_b_candidate_1 = math.inf
                    # 横の端（左）
                    if vec_short_a_b[0] != 0:
                        short_b_candidate_2 = (short.b.left_up.x - short.b.predicted_pos.x)/vec_short_a_b[0]
                    else:
                        short_b_candidate_2 = math.inf
                    # 重みから
                    short_b_candidate_3 = beta*short_diff/(alpha+beta)
                    short_b = min(short_b_candidate_1, short_b_candidate_2, short_b_candidate_3)
                    cities_move_append(cities_move_vec, short.b.idx, (vec_short_a_b[0]*short_b, vec_short_a_b[1]*short_b))
                elif short_pos_rel == "LD":# Aが左下
                    # 一番伸ばした時の角までの距離
                    alpha = short.a.predicted_pos.dist(Point(short.a.left_up.x, short.a.right_down.y))
                    beta = short.b.predicted_pos.dist(Point(short.b.right_down.x, short.b.left_up.y))
                    # 縦の端（下）
                    if vec_short_a_b[1] != 0:
                        short_a_candidate_1 = (short.a.right_down.y - short.a.predicted_pos.y)/ vec_short_a_b[1]
                    else:
                        short_a_candidate_1 = math.inf
                    # 横の端(左)
                    if vec_short_a_b[0] != 0:
                        short_a_candidate_2 = (short.a.left_up.x - short.a.predicted_pos.x)/ vec_short_a_b[0]
                    else:
                        short_a_candidate_2 = math.inf
                    # 重みから
                    short_a_candidate_3 = -alpha*short_diff/(alpha+beta)
                    short_a = min(short_a_candidate_1, short_a_candidate_2, short_a_candidate_3)
                    cities_move_append(cities_move_vec, short.a.idx, (vec_short_a_b[0]*short_a, vec_short_a_b[1]*short_a))
                    # 縦の端　（上）
                    if vec_short_a_b[1] != 0:
                        short_b_candidate_1 = (short.b.left_up.y - short.b.predicted_pos.y)/ vec_short_a_b[1]
                    else:
                        short_b_candidate_1 = math.inf
                    # 横の端　（右）
                    if vec_short_a_b[0] != 0:
                        short_b_candidate_2 = (short.b.right_down.x - short.b.predicted_pos.x)/ vec_short_a_b[0]
                    else:
                        short_b_candidate_2 = math.inf
                    # 重み付き
                    short_b_candidate_3 = beta*short_diff/(alpha+beta)
                    short_b = min(short_b_candidate_1, short_b_candidate_2, short_b_candidate_3)
                    cities_move_append(cities_move_vec, short.b.idx, (vec_short_a_b[0]*short_b, vec_short_a_b[1]*short_b))
                else: # Aが左上
                    # 一番伸ばした時の角までの距離
                    alpha = short.a.predicted_pos.dist(short.a.left_up)
                    beta = short.b.predicted_pos.dist(short.b.right_down)
                    # 縦の端 (上)
                    if vec_short_a_b[1] != 0:
                        short_a_candidate_1 = (short.a.left_up.y - short.a.predicted_pos.y)/ vec_short_a_b[1]
                    else:
                        short_a_candidate_1 = math.inf
                    # 横の端 (左)
                    if vec_short_a_b[0] != 0:
                        short_a_candidate_2 = (short.a.left_up.x - short.a.predicted_pos.x)/ vec_short_a_b[0]
                    else:
                        short_a_candidate_2 = math.inf
                    # 重み付き
                    short_a_candidate_3 = -alpha*short_diff/(alpha+beta)
                    short_a = min(short_a_candidate_1, short_a_candidate_2, short_a_candidate_3)
                    cities_move_append(cities_move_vec, short.a.idx, (vec_short_a_b[0]*short_a, vec_short_a_b[1]*short_a))
                    # 縦の端（下)
                    if vec_short_a_b[1] != 0:
                        short_b_candidate_1 = (short.b.right_down.y - short.b.predicted_pos.y)/ vec_short_a_b[1]
                    else:
                        short_b_candidate_1 = math.inf
                    # 横の端 (右)
                    if vec_short_a_b[0] != 0:
                        short_b_candidate_2 = (short.b.right_down.x - short.b.predicted_pos.x)/ vec_short_a_b[0]
                    else:
                        short_b_candidate_2 = math.inf
                    # 重み付き
                    short_b_candidate_3 = beta*short_diff/(alpha+beta)
                    short_b = min(short_b_candidate_1, short_b_candidate_2, short_b_candidate_3)
                    cities_move_append(cities_move_vec, short.b.idx, (vec_short_a_b[0]*short_b, vec_short_a_b[1]*short_b))
                
                # 長い辺について、両端の都市の移動ベクトルを設定
                # 長い辺のAB方向の単位ベクトル
                vec_long_a_b = ((long.b.predicted_pos.x - long.a.predicted_pos.x)/math.sqrt((long.b.predicted_pos.x - long.a.predicted_pos.x)**2+(long.b.predicted_pos.y - long.a.predicted_pos.y)**2),(long.b.predicted_pos.y - long.a.predicted_pos.y)/math.sqrt((long.b.predicted_pos.x - long.a.predicted_pos.x)**2+(long.b.predicted_pos.y - long.a.predicted_pos.y)**2))
                # デバッグ用出力
                print(f"long 単位ベクトル:{(vec_long_a_b[0],vec_long_a_b[1])},大きさ:{math.sqrt(vec_long_a_b[0]**2+vec_long_a_b[1]**2)}",file=sys.stderr,flush=True)
                if long_pos_rel == "RD":# Aが右下
                    # 一番縮ませた時の角までの距離
                    alpha = long.a.predicted_pos.dist(long.a.left_up)
                    beta = long.b.predicted_pos.dist(long.b.right_down)
                    # 縦の端 (上)
                    if vec_long_a_b[1] != 0:
                        long_a_candidate_1 = (long.a.left_up.y - long.a.predicted_pos.y)/ vec_long_a_b[1]
                    else:
                        long_a_candidate_1 = math.inf
                    # 横の端 (左)
                    if vec_long_a_b[0] != 0:
                        long_a_candidate_2 = (long.a.left_up.x - long.a.predicted_pos.x)/ vec_long_a_b[0]
                    else:
                        long_a_candidate_2 = math.inf
                    # 重み付き
                    long_a_candidate_3 = alpha*long_diff/(alpha+beta)
                    long_a = min(long_a_candidate_1, long_a_candidate_2, long_a_candidate_3)
                    cities_move_append(cities_move_vec, long.a.idx, (vec_long_a_b[0]*long_a, vec_long_a_b[1]*long_a))
                    # 縦の端（下)
                    if vec_long_a_b[1] != 0:
                        long_b_candidate_1 = (long.b.right_down.y - long.b.predicted_pos.y)/ vec_long_a_b[1]
                    else:
                        long_b_candidate_1 = math.inf
                    # 横の端 (右)
                    if vec_long_a_b[0] != 0:
                        long_b_candidate_2 = (long.b.right_down.x - long.b.predicted_pos.x)/ vec_long_a_b[0]
                    else:
                        long_b_candidate_2 = math.inf
                    # 重み付き
                    long_b_candidate_3 = -beta*long_diff/(alpha+beta)
                    long_b = min(long_b_candidate_1, long_b_candidate_2, long_b_candidate_3)
                    cities_move_append(cities_move_vec, long.b.idx, (vec_long_a_b[0]*long_b, vec_long_a_b[1]*long_b))
                elif long_pos_rel == "RU":# Aが右上
                    # 一番伸ばした時の角までの距離
                    alpha = long.a.predicted_pos.dist(Point(long.a.left_up.x, long.a.right_down.y))
                    beta = long.b.predicted_pos.dist(Point(long.b.right_down.x, long.b.left_up.y))
                    # 縦の端（下）
                    if vec_long_a_b[1] != 0:
                        long_a_candidate_1 = (long.a.right_down.y - long.a.predicted_pos.y)/ vec_long_a_b[1]
                    else:
                        long_a_candidate_1 = math.inf
                    # 横の端(左)
                    if vec_long_a_b[0] != 0:
                        long_a_candidate_2 = (long.a.left_up.x - long.a.predicted_pos.x)/ vec_long_a_b[0]
                    else:
                        long_a_candidate_2 = math.inf
                    # 重みから
                    long_a_candidate_3 = alpha*long_diff/(alpha+beta)
                    long_a = min(long_a_candidate_1, long_a_candidate_2, long_a_candidate_3)
                    cities_move_append(cities_move_vec, long.a.idx, (vec_long_a_b[0]*long_a, vec_long_a_b[1]*long_a))
                    # 縦の端　（上）
                    if vec_long_a_b[1] != 0:
                        long_b_candidate_1 = (long.b.left_up.y - long.b.predicted_pos.y)/ vec_long_a_b[1]
                    else:
                        long_b_candidate_1 = math.inf
                    # 横の端　（右）
                    if vec_long_a_b[0] != 0:
                        long_b_candidate_2 = (long.b.right_down.x - long.b.predicted_pos.x)/ vec_long_a_b[0]
                    else:
                        long_b_candidate_2 = math.inf
                    # 重み付き
                    long_b_candidate_3 = -beta*long_diff/(alpha+beta)
                    long_b = min(long_b_candidate_1, long_b_candidate_2, long_b_candidate_3)
                    cities_move_append(cities_move_vec, long.b.idx, (vec_long_a_b[0]*long_b, vec_long_a_b[1]*long_b))
                elif long_pos_rel == "LD":# Aが左下
                    # 一番伸ばした時の角までの距離
                    alpha = long.a.predicted_pos.dist(Point(long.a.right_down.x, long.a.left_up.y))
                    beta = long.b.predicted_pos.dist(Point(long.b.left_up.x, long.b.right_down.y))
                    # 縦の端（上）
                    if vec_long_a_b[1] != 0:
                        long_a_candidate_1 = (long.a.left_up.y - long.a.predicted_pos.y)/vec_long_a_b[1]
                    else:
                        long_a_candidate_1 = math.inf
                    # 横の端 (右)
                    if vec_long_a_b[0] != 0:
                        long_a_candidate_2 = (long.a.right_down.x - long.a.predicted_pos.x)/vec_long_a_b[0]
                    else:
                        long_a_candidate_2 = math.inf
                    # 重みから
                    long_a_candidate_3 = alpha*long_diff/(alpha+beta)
                    long_a = min(long_a_candidate_1, long_a_candidate_2, long_a_candidate_3)
                    cities_move_append(cities_move_vec, long.a.idx, (vec_long_a_b[0]*long_a, vec_long_a_b[1]*long_a))
                    # 縦の端（下）
                    if vec_long_a_b[1] != 0:
                        long_b_candidate_1 = (long.b.right_down.y - long.b.predicted_pos.y)/vec_long_a_b[1]
                    else:
                        long_b_candidate_1 = math.inf
                    # 横の端（左）
                    if vec_long_a_b[0] != 0:
                        long_b_candidate_2 = (long.b.left_up.x - long.b.predicted_pos.x)/vec_long_a_b[0]
                    else:
                        long_b_candidate_2 = math.inf
                    # 重みから
                    long_b_candidate_3 = -beta*long_diff/(alpha+beta)
                    long_b = min(long_b_candidate_1, long_b_candidate_2, long_b_candidate_3)
                    cities_move_append(cities_move_vec, long.b.idx, (vec_long_a_b[0]*long_b, vec_long_a_b[1]*long_b))                    
                else: # Aが左上
                    # 一番伸ばした時の角までの距離
                    alpha = long.a.predicted_pos.dist(long.a.right_down)
                    beta = long.b.predicted_pos.dist(long.b.left_up)
                    # 単位ベクトルにかける定数のうち、横の端、縦の端、重みから考える定数の中から一番小さいものを選ぶ
                    # 縦の端（下）
                    if vec_long_a_b[1] != 0:
                        long_a_candidate_1 = (long.a.right_down.y - long.a.predicted_pos.y)/vec_long_a_b[1]
                    else:
                        long_a_candidate_1 = math.inf
                    # 横の端（右）
                    if vec_long_a_b[0] != 0:
                        long_a_candidate_2 = (long.a.right_down.x - long.a.predicted_pos.x)/vec_long_a_b[0]
                    else:
                        long_a_candidate_2 = math.inf
                    # 重みから
                    long_a_candidate_3 = alpha*long_diff/(alpha+beta)
                    long_a = min(long_a_candidate_1,long_a_candidate_2,long_a_candidate_3)
                    # 短い辺の都市Aに対する移動するべき方向のベクトルを追加
                    cities_move_append(cities_move_vec, long.a.idx, (vec_long_a_b[0]*long_a, vec_long_a_b[1]*long_a))
                    # 縦の端（上）
                    if vec_long_a_b[1] != 0:
                        long_b_candidate_1 = (long.b.left_up.y - long.b.predicted_pos.y)/vec_long_a_b[1]
                    else:
                        long_b_candidate_1 = math.inf
                    # 横の端　(左)
                    if vec_long_a_b[0] != 0:
                        long_b_candidate_2 = (long.b.left_up.x - long.b.predicted_pos.x)/vec_long_a_b[0]
                    else:
                        long_b_candidate_2 = math.inf
                    # 重みから
                    long_b_candidate_3 = -beta*long_diff/(alpha+beta)
                    long_b = min(long_b_candidate_1, long_b_candidate_2, long_b_candidate_3)
                    # 短い辺の都市Bに対する移動するべき方向のベクトルを追加
                    cities_move_append(cities_move_vec, long.b.idx, (vec_long_a_b[0]*long_b, vec_long_a_b[1]*long_b))

            # 大小関係が正しかった場合
            else:
                # 二つの辺の両端の合計4点に対して移動するべき方向のベクトルを追加する
                cities_move_append(cities_move_vec, short.a.idx, (0, 0))
                cities_move_append(cities_move_vec, short.b.idx, (0, 0))
                cities_move_append(cities_move_vec, long.a.idx, (0, 0))
                cities_move_append(cities_move_vec, long.b.idx, (0, 0))

    return count,cities_move_vec


def point_update(input_data: Input):
    """
    都市の予測位置を正しい位置に近づけていく関数
    
    Args:
        input_data (Input): 入力データ
    
    Returns:
        None
    """
    # loop_countは基本400
    loop_count = input_data.max_query_count
    # 3~15
    query_city_count = input_data.query_max_cities_size
    cities = input_data.cities
    query_ans = []
    # 各都市の動くべき方向のベクトルの配列
    cities_move_vec = [(0.0, 0.0, 0) for _ in range(len(input_data.cities))]
    for _ in range(loop_count):
        candidate_cities = []
        # 都市を最大数だけランダムに選ぶ
        while len(candidate_cities) < query_city_count:
            rand_city = random.choice(cities)
            if rand_city not in candidate_cities:
                candidate_cities.append(rand_city)
        # 占いをして、制約の配列に追加
        query_ans.append(forecast(candidate_cities))

    # デバッグ用出力
    #for edge in query_ans[0]:  # 最初のクエリのエッジを確認
    #    print(f"Edge A ID: {id(edge.a)}, Edge B ID: {id(edge.b)}", file=sys.stderr)
    #    print(f"City A ID: {id(input_data.cities[edge.a.idx])}, City B ID: {id(input_data.cities[edge.b.idx])}", file=sys.stderr)

    # 現在のスコアを初期化
    current_score,cities_move_vec = count_contradiction(query_ans,cities_move_vec,cities)
    random.seed(42)
    start_time = time.time()
    time_limit = 10.0
    start_temperature = 2e2
    end_temperature = 1e0
    current_temperature = start_temperature
    iteration = 0
    # 焼きなまし法
    while True:
        current_time = time.time()
        if current_time - start_time > time_limit:
            break
        if current_score == 0:
            break
        if iteration == 1:
            break
        # すべての都市を微調整する
        old_x = [0]*len(input_data.cities)
        old_y = [0]*len(input_data.cities)
        old_move_vec = [0]*len(input_data.cities)
        rand = random.random()
        # デバッグ用出力
        print(f"変更前city0:{cities[0].predicted_pos}",file=sys.stderr,flush=True)
        print(f"変更する足される量:{(cities_move_vec[0][0]*rand,cities_move_vec[0][1]*rand)}",file=sys.stderr,flush=True)
        for i in range(len(input_data.cities)):
            old_x[i] = cities[i].predicted_pos.x
            old_y[i] = cities[i].predicted_pos.y
            old_move_vec[i] = cities_move_vec[i]
            cities[i].predicted_pos.x += rand*cities_move_vec[i][0]
            cities[i].predicted_pos.y += rand*cities_move_vec[i][1]
        # デバッグ用出力
        print(f"変更後座標:{cities[0].predicted_pos}",file=sys.stderr,flush=True)
        # スコアの再計算
        new_score, _ = count_contradiction(query_ans, cities_move_vec,cities)
        #デバッグ用出力
        print(f"current_score:{int(current_score)}, new_score:{int(new_score)}",file=sys.stderr,flush=True)
        delta_score = new_score - current_score
        # 良くなるか悪くなっても確率で採用
        if delta_score <= 0 or random.random() < 2:#math.exp(-delta_score / current_temperature):
            current_score = new_score
        # でなければ元に戻す
        else:
            for i in range(len(input_data.cities)):
                cities[i].predicted_pos.x = old_x[i]
                cities[i].predicted_pos.y = old_y[i]
                cities_move_vec[i] = old_move_vec[i]
        iteration += 1
        # 1000回ごとに進捗を出力
        if iteration % 1000 == 0:
            print(f"iteration: {iteration}, score: {current_score}",file=sys.stderr, flush=True)
        progress = (current_time - start_time) / time_limit
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
    print(f"iteration: {iteration}, score: {current_score}",file=sys.stderr, flush=True)
    # デバッグ用出力
    #print(f"city0の予測位置:{cities[0].predicted_pos}",file=sys.stderr, flush=True)
    return


def solve(input_data: Input) -> Output:
    """
    問題を解く関数
    
    Args:
        input_data (Input): 入力データ
    
    Returns:
        Output: 出力データ
    """
    # 解法5
    # 最大都市数のクエリを最大回数繰り返す
    # ランダムに都市を選び、クエリに対して矛盾がなくなるまたは時間で山登り
    # 候補の中で一番左のものをとり、グループに入れる
    # そこから近い順にグループ内の都市の数だけ取る。
    # これを繰り返してグループ分けをする
    # グループの都市数が１以上のグループからランダムにグループを2つ選び、
    # ランダムな都市同士を交換する。グループのスコアの変化を見て、
    # 焼きなましする。
    # グループ内の都市についてクラスカル法でつなぐ

    # 都市の位置をある程度絞る
    point_update(input_data)

    group_list = [] #groupの配列

    cities = input_data.cities

    # デバッグ用出力
    #print(f"city0の予測位置2:{cities[0].predicted_pos}",file=sys.stderr, flush=True)
    # デバッグ用出力
    #for city in cities:
    #    print(f"都市のインデックス:{city.idx},都市の中心座標{(int(city.left_up.x+city.right_down.x/2),int(city.left_up.y+city.right_down.y))},都市の予測座標{(int(city.predicted_pos.x),int(city.predicted_pos.y))}",file=sys.stderr,flush=True)
    #ソートした都市の配列を候補として使う
    sorted_cities = deque(sorted(input_data.cities, key=lambda city: (city.predicted_pos.x, city.predicted_pos.y)))

    # グループ分けをする
    for i in range(input_data.group_count):
        # グループを作成
        group = Group(i)
        g_c_count = input_data.group_cities_count[i]
        # 先頭の要素を現在位置に設定
        current_city = sorted_cities.popleft()
        current_pos = current_city.predicted_pos
        group.add_city(current_city)
        # 現在位置から近いものをsorted_citiesからg_c_count-1個選ぶ
        # 選んだものはsorted_citiesから削除する
        sorted_by_distance = sorted(sorted_cities, key=lambda city: current_pos.dist(city.predicted_pos))
        # 選んだものをグループに追加し、sorted_citiesから削除
        for j in range(g_c_count-1):
            group.add_city(sorted_by_distance[j])
            # デバッグ用
            #print(f"group_add:{sorted_by_distance[j].idx}",file=sys.stderr,flush=True)
            sorted_cities.remove(sorted_by_distance[j])
        group_list.append(group)

    # ここで焼きなまし法
    random.seed(42)
    # 開始時刻を取得
    start_time = time.time()
    # 制限時間
    time_limit = 1.1-(start_time - global_start_time)
    # 開始温度と終了温度
    start_temperature = 1e2
    end_temperature = 1e0

    # 現在のスコアを計算
    current_score = 0
    for group in group_list:
        current_score += group.calculate_score()

    # 現在の温度
    current_temperature = start_temperature

    # 試行回数
    iteration = 0

    #本体
    while True:
        # 現在時刻を取得
        current_time = time.time()

        #制限時間になったら終了
        if current_time - start_time >= time_limit:
            break

        # グループの都市の数が１以上の中からランダムで2つ選ぶ
        i = random.randint(0,len(group_list)-1)
        if len(group_list[i].cities) == 0:
            while len(group_list[i].cities) == 0:
                i = random.randint(0,len(group_list)-1)
        j = random.randint(0,len(group_list)-1)
        if len(group_list[j].cities) == 0:
            while len(group_list[j].cities) == 0:
                j = random.randint(0,len(group_list)-1)
        
        before_score = group_list[i].calculate_score()+group_list[j].calculate_score()

        # グループiとグループjのランダムな都市を交換して、操作後のスコアを求める
        i_city = random.choice(group_list[i].cities)
        j_city = random.choice(group_list[j].cities)
        if i_city == j_city:
            continue
        group_list[i].remove_city(i_city)
        group_list[j].remove_city(j_city)

        group_list[i].add_city(j_city)
        group_list[j].add_city(i_city)

        after_score = group_list[i].calculate_score()+group_list[j].calculate_score()
        delta_score = after_score - before_score
        if delta_score <= 0:
            current_score += delta_score
        else:
            if random.random() < math.exp(-delta_score / current_temperature):
                current_score += delta_score
            else:
                group_list[j].remove_city(i_city)
                group_list[i].remove_city(j_city)
                group_list[i].add_city(i_city)
                group_list[j].add_city(j_city)
        
        # 試行回数のカウントを増やす
        # 進行状況を可視化するため、一定回数ごとに現在の試行回数とスコアを出力する
        iteration += 1
        if iteration % 10000 == 0:
            print(f"iteration: {iteration}, score: {current_score}",file=sys.stderr)
        
        # 現在の経過時間の割合を計算する
        progress = (current_time - start_time) / time_limit

        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
    print(f"iteration:{iteration}, score: {current_score}",file=sys.stderr)

    # 各グループでルートを作る
    for group in group_list:
        # インデックスのマッピングを作成
        local_index_map = {city.idx: idx for idx, city in enumerate(group.cities)}
        reverse_index_map = {idx: city.idx for idx, city in enumerate(group.cities)}
        g_c_count = len(group.cities)

        # グループ内の都市が5つ以上の時、ドロネー三角形分割を利用して最小全域木を作成する
        if g_c_count >= 5:
            # グループ内の都市の座標を取得
            points = [[city.predicted_pos.x, city.predicted_pos.y] for city in group.cities]

            # ドロネー三角形分割を使用して辺の候補を取得
            delaunay = Delaunay(points)
            edges = set()
            for simplex in delaunay.simplices:
                for i in range(3):
                    a, b = simplex[i], simplex[(i + 1) % 3]
                    # 都市のインデックスを取得して辺を作成
                    idx_a = group.cities[a].idx
                    idx_b = group.cities[b].idx
                    edges.add((min(idx_a, idx_b), max(idx_a, idx_b)))  # 辺を一意に識別するためにソートして格納
            # グループ内の都市について最小全域木を作成する
            edge_list = []
            for idx_a, idx_b in edges:
                predicted_distance = group.cities[local_index_map[idx_a]].predicted_pos.dist(
                    group.cities[local_index_map[idx_b]].predicted_pos
                )
                heapq.heappush(edge_list, (predicted_distance, local_index_map[idx_a], local_index_map[idx_b]))
        else:
            # グループ内の都市が4つ以下の場合、すべての辺を探索する
            edge_list = []
            for k in group.cities:
                for l in group.cities:
                    if k.idx < l.idx:
                        predicted_distance = k.predicted_pos.dist(l.predicted_pos)
                        heapq.heappush(edge_list, (predicted_distance, local_index_map[k.idx], local_index_map[l.idx]))
        uf = UnionFind(g_c_count)
        while edge_list:
            predicted_distance, node1, node2 = heapq.heappop(edge_list)
            if not uf.same(node1, node2):
                uf.unite(node1, node2)
                group.edges.append(Edge(cities[reverse_index_map[node1]], cities[reverse_index_map[node2]]))

    return Output(group_list)

def main():
    global global_start_time
    global_start_time = time.time()
    # 入力データを受け取る
    input_data = Input.read()

    #問題を解く
    output_data = solve(input_data)

    # 出力する
    output_data.print_output()

if __name__ == "__main__":
    main()