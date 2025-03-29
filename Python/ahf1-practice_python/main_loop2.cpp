#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <chrono>
#include <set>
#include <cassert>
#include <ctime>
#include <iomanip>

// 注文の焼きなまし後、ルートの焼きなまし
const int PRIME_NUMBER = 998244353;
const int BASE = 10007;

// グローバル変数
std::chrono::high_resolution_clock::time_point global_start_time;
std::vector<int> candidates;

// ハッシュ関数
int get_hash(int x, int y, int idx, int tp) {
    return (x + y * BASE + idx * static_cast<long long>(std::pow(BASE, 2)) % PRIME_NUMBER + 
            tp * static_cast<long long>(std::pow(BASE, 3)) % PRIME_NUMBER) % PRIME_NUMBER;
}

// 2次元座標上の点を表すクラス
class Point {
public:
    int x, y;

    Point(int x = 0, int y = 0) : x(x), y(y) {}

    // マンハッタン距離を計算
    int dist(const Point& p) const {
        return std::abs(x - p.x) + std::abs(y - p.y);
    }
};

// レストランを表すクラス
class Restaurant : public Point {
public:
    int idx;

    Restaurant(int x, int y, int idx) : Point(x, y), idx(idx) {}

    size_t hash() const {
        return get_hash(x, y, idx, 0);
    }
};

// 目的地を表すクラス
class Destination : public Point {
public:
    int idx;

    Destination(int x, int y, int idx) : Point(x, y), idx(idx) {}

    size_t hash() const {
        return get_hash(x, y, idx, 1);
    }
};

// 入力データを表すクラス
class Input {
public:
    int order_count;
    int pickup_count;
    Point office;
    std::vector<Point> restaurants;
    std::vector<Point> destinations;

    static Input read() {
        Input input;
        input.order_count = 1000;
        input.pickup_count = 50;
        input.office = Point(400, 400);

        for (int i = 0; i < input.order_count; ++i) {
            int a, b, c, d;
            std::cin >> a >> b >> c >> d;
            input.restaurants.emplace_back(a, b);
            input.destinations.emplace_back(c, d);
        }

        return input;
    }
};

// 出力データを表すクラス
class Output {
public:
    int dist_sum;
    std::vector<int> orders;
    std::vector<Point> route;

    Output(const std::vector<int>& orders, const std::vector<Point>& route) : orders(orders), route(route) {
        // 移動距離の合計を計算する
        dist_sum = 0;
        for (size_t i = 0; i < route.size() - 1; ++i) {
            dist_sum += route[i].dist(route[i + 1]);
        }
    }

    void print_output() {
        // 選択した注文の集合を出力する
        std::cout << orders.size() << " ";
        for (size_t i = 0; i < orders.size(); ++i) {
            std::cout << orders[i] + 1 << " ";
        }
        std::cout << std::endl;

        // 配達ルートを出力する
        std::cout << route.size();
        for (const auto& p : route) {
            std::cout << " " << p.x << " " << p.y;
        }
        std::cout << std::endl;
    }
};

// 貪欲解法
Output solve_greedy(const Input& input_data, const std::vector<int>& selected_orders) {
    std::vector<Point> route;
    Point current_position(400, 400);  // オフィスから開始
    route.push_back(current_position);
    
    std::set<Restaurant> visitables;
    for (int order : selected_orders) {
        visitables.insert(Restaurant(
            input_data.restaurants[order].x, 
            input_data.restaurants[order].y, 
            order
        ));
    }
    
    while (!visitables.empty()) {
        int min_dist = std::numeric_limits<int>::max();
        Restaurant next_position(0, 0, -1);
        
        for (const auto& visitable : visitables) {
            int dist = current_position.dist(visitable);
            if (dist < min_dist) {
                min_dist = dist;
                next_position = visitable;
            }
        }
        
        route.push_back(next_position);
        
        // If restaurant is visited, add corresponding destination
        visitables.erase(next_position);
        visitables.insert(Destination(
            input_data.destinations[next_position.idx].x,
            input_data.destinations[next_position.idx].y,
            next_position.idx
        ));
        
        current_position = next_position;
    }
    
    route.push_back(Point(400, 400));  // オフィスに帰る
    
    assert(is_valid_order(route));
    return Output(selected_orders, route);
}

// 経路が有効かどうかをチェックする関数
bool is_valid_order(const std::vector<Point>& route) {
    std::set<int> got_restaurants;
    for (const auto& point : route) {
        const Restaurant* restaurant = dynamic_cast<const Restaurant*>(&point);
        const Destination* destination = dynamic_cast<const Destination*>(&point);
        
        if (restaurant) {
            got_restaurants.insert(restaurant->idx);
        }
        if (destination) {
            if (got_restaurants.find(destination->idx) == got_restaurants.end()) {
                return false;
            }
        }
    }
    return true;
}

// 経路の距離を計算する関数
int get_distance(const std::vector<Point>& route) {
    int dist = 0;
    for (size_t i = 0; i < route.size() - 1; ++i) {
        dist += route[i].dist(route[i + 1]);
    }
    return dist;
}



// 焼きなまし法のための乱数ジェネレータをグローバルに定義
std::mt19937 rng(42);


// 効率的な焼きなまし法関数
Output solve_efficient_annealing(const Input& input_data, const Output& output_data_greedy) {
    // 初期解の取得
    std::set<int> current_orders(output_data_greedy.orders.begin(), output_data_greedy.orders.end());
    std::vector<Point> current_route = output_data_greedy.route;
    int current_dist = get_distance(current_route);
    
    // 最良解の追跡用変数
    std::vector<int> best_orders(current_orders.begin(), current_orders.end());
    std::vector<Point> best_route = current_route;
    int best_dist = current_dist;
    
    // 焼きなまし法のパラメータ
    double start_temperature = 50.0;
    double end_temperature = 1.0;
    double current_temperature = start_temperature;
    
    // 時間制限
    double time_limit = 1.5;
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // 乱数生成器の設定
    std::mt19937 rng(42);
    std::uniform_real_distribution<> dist(0.0, 1.0);
    std::uniform_int_distribution<> order_dist(0, candidates.size() - 1);
    
    int iteration = 0;
    while (true) {
        auto current_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = current_time - global_start_time;
        
        // 時間制限チェック
        if (elapsed.count() >= time_limit) break;
        
        // ランダムに削除する注文と追加する注文を選択
        int remove_order = *std::next(current_orders.begin(), 
            std::uniform_int_distribution<>(0, current_orders.size() - 1)(rng));
        
        int add_order = candidates[order_dist(rng)];
        while (current_orders.count(add_order) > 0) {
            add_order = candidates[order_dist(rng)];
        }
        
        // 新しい注文セットの作成
        std::set<int> new_orders = current_orders;
        new_orders.erase(remove_order);
        new_orders.insert(add_order);
        
        // 新しい経路の生成と距離計算
        std::vector<int> new_orders_vec(new_orders.begin(), new_orders.end());
        Output output = solve_greedy(input_data, new_orders_vec);
        int new_dist = get_distance(output.route);
        
        // 受理基準
        if (new_dist <= current_dist || dist(rng) <= std::exp((current_dist - new_dist) / current_temperature)) {
            current_orders = new_orders;
            current_route = output.route;
            current_dist = new_dist;
            
            // 最良解の更新
            if (current_dist < best_dist) {
                best_dist = current_dist;
                best_route = current_route;
                best_orders = std::vector<int>(current_orders.begin(), current_orders.end());
            }
        }
        
        // 温度の更新
        double progress = elapsed.count() / time_limit;
        current_temperature = std::pow(start_temperature, 1.0 - progress) * 
                               std::pow(end_temperature, progress);
        
        iteration++;
        if (iteration % 1000 == 0) {
            std::cerr << "iteration: " << iteration 
                      << ", total distance: " << current_dist << std::endl;
        }
    }
    
    std::cerr << "---Result---" << std::endl;
    std::cerr << "iteration: " << iteration 
              << ", total_distance: " << best_dist << std::endl;
    
    return Output(best_orders, best_route);
}

// 更新距離関数
int update_distance(std::vector<Point>& route, int i, int j) {
    if (i == j) return 0;
    
    int before, after;
    if (i > j) {
        before = route[j].dist(route[j-1]) + route[i].dist(route[i-1]) + route[i+1].dist(route[i]);
        after = route[i].dist(route[j]) + route[i].dist(route[j-1]) + route[i-1].dist(route[i+1]);
    } else {
        before = route[j+1].dist(route[j]) + route[i].dist(route[i-1]) + route[i+1].dist(route[i]);
        after = route[j+1].dist(route[i]) + route[j].dist(route[i]) + route[i+1].dist(route[i-1]);
    }
    
    return after - before;
}

// インデックス更新関数
void update_index(std::unordered_map<int, int>& destination_dict, 
                  std::unordered_map<int, int>& restaurant_dict, 
                  int i, int j) {
    if (i < j) {
        for (auto& [key, value] : destination_dict) {
            if (value > i && value <= j) value--;
        }
        for (auto& [key, value] : restaurant_dict) {
            if (value > i && value <= j) value--;
        }
    } else if (i > j) {
        for (auto& [key, value] : destination_dict) {
            if (value < i && value >= j) value++;
        }
        for (auto& [key, value] : restaurant_dict) {
            if (value < i && value >= j) value++;
        }
    }
}


// シミュレーテッドアニーリング
Output solve_simulated_annealing(const Input& input_data, const Output& output_data_greedy) {
    // 初期解のコピー
    std::vector<int> orders = output_data_greedy.orders;
    std::vector<Point> route = output_data_greedy.route;
    
    // インデックス辞書の初期化
    std::unordered_map<int, int> restaurant_dict;
    std::unordered_map<int, int> destination_dict;
    
    for (int order : orders) {
        restaurant_dict[order] = std::find_if(route.begin(), route.end(), 
            [&](const Point& p) { 
                auto r = dynamic_cast<const Restaurant*>(&p);
                return r && r->idx == order;
            }) - route.begin();
        
        destination_dict[order] = std::find_if(route.begin(), route.end(), 
            [&](const Point& p) { 
                auto d = dynamic_cast<const Destination*>(&p);
                return d && d->idx == order;
            }) - route.begin();
    }
    
    // 現在の解と最良解の初期化
    int current_dist = get_distance(route);
    int best_dist = current_dist;
    std::vector<Point> best_route = route;
    
    // 乱数生成器の設定
    std::uniform_real_distribution<> dist(0.0, 1.0);
    
    // 焼きなまし法のパラメータ
    double start_temperature = 50.0;
    double end_temperature = 1.0;
    
    // 時間制限
    auto start_time = std::chrono::high_resolution_clock::now();
    double time_limit = 1.78;
    
    int iteration = 0;
    while (true) {
        auto current_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = current_time - start_time;
        
        // 制限時間チェック
        if (elapsed.count() >= time_limit) break;
        
        // 温度計算
        double progress = elapsed.count() / time_limit;
        double current_temperature = std::pow(start_temperature, 1.0 - progress) * 
                                      std::pow(end_temperature, progress);
        
        // ランダムな注文選択
        int rand_order = orders[std::uniform_int_distribution<>(0, orders.size() - 1)(rng)];
        
        // 交換操作
        if (iteration % 2 == 0) {
            // レストランを選んで配達先よりも前に挿入
            int i = restaurant_dict[rand_order];
            int j = std::uniform_int_distribution<>(1, destination_dict[rand_order] - 1)(rng);
            
            int delta = update_distance(route, i, j);
            if (delta <= 0 || dist(rng) < std::exp(-delta / current_temperature)) {
                update_index(destination_dict, restaurant_dict, i, j);
                restaurant_dict[rand_order] = j;
                
                Point point_to_move = route[i];
                route.erase(route.begin() + i);
                route.insert(route.begin() + j, point_to_move);
                
                current_dist += delta;
                if (current_dist < best_dist) {
                    best_dist = current_dist;
                    best_route = route;
                }
            }
        } else {
            // 配達先を選んでレストランよりも後に挿入
            int i = destination_dict[rand_order];
            int j = std::uniform_int_distribution<>(restaurant_dict[rand_order] + 1, 2 * input_data.pickup_count)(rng);
            
            int delta = update_distance(route, i, j);
            if (delta <= 0 || dist(rng) < std::exp(-delta / current_temperature)) {
                update_index(destination_dict, restaurant_dict, i, j);
                destination_dict[rand_order] = j;
                
                Point point_to_move = route[i];
                route.erase(route.begin() + i);
                route.insert(route.begin() + j, point_to_move);
                
                current_dist += delta;
                if (current_dist < best_dist) {
                    best_dist = current_dist;
                    best_route = route;
                }
            }
        }
        
        // 進捗出力
        iteration++;
        if (iteration % 1000 == 0) {
            std::cerr << "iteration: " << iteration 
                      << ", total distance: " << current_dist << std::endl;
        }
    }
    
    // 結果出力
    std::cerr << "--- Result ---" << std::endl;
    std::cerr << "iteration     : " << iteration << std::endl;
    std::cerr << "total distance: " << best_dist << std::endl;
    
    return Output(orders, best_route);
}

// 関数プロトタイプ宣言
Output solve_greedy(const Input& input_data, const std::vector<int>& selected_orders);
Output solve_simulated_annealing(const Input& input_data, const Output& output_data_greedy);

int main() {
    // 開始時刻を取得
    global_start_time = std::chrono::high_resolution_clock::now();

    // 入力データを受け取る
    Input input_data = Input::read();

    // 注文をソート
    std::vector<int> sorted_orders(input_data.order_count);
    std::iota(sorted_orders.begin(), sorted_orders.end(), 0);
    std::sort(sorted_orders.begin(), sorted_orders.end(), [&](int a, int b) {
        return std::max(Point(400, 400).dist(input_data.restaurants[a]), 
                        Point(400, 400).dist(input_data.destinations[a])) <
               std::max(Point(400, 400).dist(input_data.restaurants[b]), 
                        Point(400, 400).dist(input_data.destinations[b]));
    });

    // 候補注文の選択
    for (int i = 0; i < input_data.order_count; ++i) {
        if (input_data.office.dist(input_data.restaurants[i]) <= 350 && 
            input_data.office.dist(input_data.destinations[i]) <= 350) {
            candidates.push_back(i);
        }
    }

    // 最初の注文選択
    std::vector<int> first_selected_orders(sorted_orders.begin(), 
                                           sorted_orders.begin() + input_data.pickup_count);

    // 解の改善
    Output output_data_greedy = solve_greedy(input_data, first_selected_orders);
    Output output_data = solve_simulated_annealing(input_data, output_data_greedy);

    // 出力する
    output_data.print_output();

    return 0;
}