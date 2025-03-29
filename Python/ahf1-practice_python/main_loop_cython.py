"""
Cythonを使用して高速化した注文の焼きなまし後、ルートの焼きなまし
"""

import math
import random
import sys
import time
from dataclasses import dataclass
from typing import List
from libc.math cimport abs

# 開始時刻を取得
global_start_time = time.time()
candidates = []
cdef int prime_number = 998244353
cdef int base = 10007

cdef int get_hash(int x, int y, int idx, int tp):
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
    restaurants: List[Point]
    destinations: List[Point]
    
    @staticmethod
    def read() -> 'Input':
        """
        入力データを読み込む
        """
        cdef int order_count = 1000
        cdef int pickup_count = 50
        cdef Point office = Point(400, 400)
        cdef list restaurants = []
        cdef list destinations = []
        
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
    orders: List[int]
    route: List[Point]
    
    def __init__(self, orders: List[int], route: List[Point]):
        self.orders = list(orders)
        self.route = list(route)
        self.dist_sum = 0
        
        for i in range(len(route) - 1):
            self.dist_sum += route[i].dist(route[i + 1])
    
    def print_output(self):
        """
        解を出力する
        """
        print(len(self.orders), end=" ")
        print(" ".join(map(lambda x: str(x + 1), self.orders)))
        print(len(self.route), end="")
        for p in self.route:
            print(f" {p.x} {p.y}", end="")
        print()

def solve_greedy(Input input_data, List[int] selected_orders) -> Output:
    """
    貪欲法で問題を解く
    """
    cdef list route = []
    cdef Point current_position = Point(400, 400)
    cdef set visitables = {
        Restaurant(
            input_data.restaurants[i].x,
            input_data.restaurants[i].y,
            i
        ) for i in selected_orders
    }
    cdef int min_dist
    cdef Point next_position

    route.append(current_position)
    
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
    
    route.append(Point(400, 400))
    assert is_valid_order(route)
    return Output(selected_orders, route)

def is_valid_order(List[Point] route) -> bool:
    """
    注文が配達可能か判定する
    """
    cdef set got_restaurants = set()
    for i in range(len(route)):
        if isinstance(route[i], Restaurant):
            got_restaurants.add(route[i].idx)
        if isinstance(route[i], Destination):
            if route[i].idx not in got_restaurants:
                return False
    return True

def get_distance(List[Point] route) -> int:
    """
    経路の距離を計算する
    """
    cdef int dist = 0
    for i in range(len(route) - 1):
        dist += route[i].dist(route[i + 1])
    return dist

def solve_efficient_annealing(Input input_data, Output output_data_greedy) -> Output:
    """
    効率的な焼きなまし法で経路を最適化する
    """
    current_orders = set(output_data_greedy.orders)
    current_route = output_data_greedy.route
    current_dist = get_distance(current_route)
    
    best_orders = list(current_orders)
    best_route = current_route
    best_dist = current_dist
    
    start_temperature = 50
    end_temperature = 1
    current_temperature = start_temperature
    
    time_limit = 1.5
    start_time = time.time()
    
    random.seed(42)
    iteration = 0
    
    while time.time() - global_start_time < time_limit:
        remove_order = random.choice(list(current_orders))
        add_order = random.choice(candidates)
        
        while add_order in current_orders:
            add_order = random.choice(candidates)
        
        new_orders = current_orders.copy()
        new_orders.remove(remove_order)
        new_orders.add(add_order)
        
        output = solve_greedy(input_data, list(new_orders))
        new_dist = get_distance(output.route)
        
        if new_dist <= current_dist or random.random() <= math.exp((current_dist - new_dist) / current_temperature):
            current_orders = new_orders
            current_route = output.route
            current_dist = new_dist
            
            if current_dist < best_dist:
                best_dist = current_dist
                best_route = current_route
                best_orders = list(current_orders)
        
        progress = (time.time() - start_time) / time_limit
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
        
        iteration += 1
        if iteration % 1000 == 0:
            print(f"iteration: {iteration}, total distance: {current_dist}", file=sys.stderr)
    print("---Result---", file=sys.stderr)
    print(f"iteration: {iteration}, total_distance: {best_dist}", file=sys.stderr)
    return Output(best_orders, best_route)

def update_distance(List[Point] route, int i, int j) -> int:
    """
    経路の距離を更新する
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

def update_index(dict[int, int] destination_dict, dict[int, int] restaurant_dict, int i, int j):
    """
    i番目とj番目の間のレストランと配達先のインデックスを更新する
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

def solve_simulated_annealing(Input input_data, Output output_data_greedy) -> Output:
    """
    焼きなまし法で配達先の訪問順序を改善する
    """
    orders = list(output_data_greedy.orders)
    route = list(output_data_greedy.route)
    current_dist = get_distance(route)
    
    best_orders = list(orders)
    best_route = list(route)
    best_dist = current_dist
    
    random.seed(42)
    start_time = time.time()
    
    restaurant_dict = {order: route.index(Restaurant(input_data.restaurants[order].x, input_data.restaurants[order].y, order)) for order in orders}
    destination_dict = {order: route.index(Destination(input_data.destinations[order].x, input_data.destinations[order].y, order)) for order in orders}
    
    time_limit = 1.78 - (start_time - global_start_time)
    start_temperature = 1e1
    end_temperature = 1e0
    current_temperature = start_temperature
    
    iteration = 0
    
    while True:
        current_time = time.time()
        if current_time - start_time >= time_limit:
            break
        rand_orders = random.choice(orders)
        if iteration & 1:
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
        else:
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
        iteration += 1
        progress = (current_time - start_time) / time_limit
        current_temperature = start_temperature ** (1.0 - progress) * end_temperature ** progress
    print("--- Result ---", file=sys.stderr)
    print("iteration     :", iteration, file=sys.stderr)
    print("total distance:", best_dist, file=sys.stderr)
    return Output(best_orders, best_route)

def main():
    global candidates
    input_data = Input.read()
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
    first_selected_orders = sorted_orders[:input_data.pickup_count]
    output_data_greedy = solve_greedy(input_data, first_selected_orders)
    output_data_sa = solve_efficient_annealing(input_data, output_data_greedy)
    output_data = solve_simulated_annealing(input_data, output_data_sa)
    output_data.print_output()

if __name__ == "__main__":
    main()
