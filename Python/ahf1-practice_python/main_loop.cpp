#include <iostream>
#include <vector>
#include <set>
#include <string>
#include <cmath>
#include <chrono>
#include <cstdlib>
#include <cassert>
#include <iomanip>
#include <map>
#include <algorithm>
#include <climits>
#include <numeric>
#include <random>

using namespace std;
using namespace std::chrono;

// 定数
const int PRIME_NUMBER = 998244353;
const int BASE = 10007;

// グローバル変数
vector<int> candidates;

// ハッシュ関数
int get_hash(int x, int y, int idx, int tp) {
    return (x + y * BASE + idx * static_cast<int>(pow(BASE, 2)) + tp * static_cast<int>(pow(BASE, 3))) % PRIME_NUMBER;
}

// Pointクラス
class Point {
public:
    int x, y;

    Point(int x = 0, int y = 0) : x(x), y(y) {}

    virtual ~Point() {}

    int dist(const Point& p) const {
        return abs(x - p.x) + abs(y - p.y);
    }
};

// Restaurantクラス
class Restaurant : public Point {
public:
    int idx;

    Restaurant(int x, int y, int idx) : Point(x, y), idx(idx) {}

    bool operator<(const Restaurant& other) const {
        return tie(x, y, idx) < tie(other.x, other.y, other.idx);
    }
};

class Destination : public Point {
public:
    int idx;

    Destination(int x, int y, int idx) : Point(x, y), idx(idx) {}

    bool operator<(const Destination& other) const {
        return tie(x, y, idx) < tie(other.x, other.y, other.idx);
    }
};

// Inputクラス
class Input {
public:
    int order_count;
    int pickup_count;
    Point office;
    vector<Point> restaurants;
    vector<Point> destinations;

    Input(int order_count, int pickup_count, Point office, vector<Point> restaurants, vector<Point> destinations)
        : order_count(order_count), pickup_count(pickup_count), office(office), restaurants(restaurants), destinations(destinations) {}

    static Input read() {
        int order_count = 1000;
        int pickup_count = 50;
        Point office(400, 400);
        vector<Point> restaurants;
        vector<Point> destinations;

        for (int i = 0; i < order_count; ++i) {
            int a, b, c, d;
            cin >> a >> b >> c >> d;
            restaurants.emplace_back(a, b);
            destinations.emplace_back(c, d);
        }

        return Input(order_count, pickup_count, office, restaurants, destinations);
    }
};

// Outputクラス
class Output {
public:
    int dist_sum;
    vector<int> orders;
    vector<Point> route;

    Output(const vector<int>& orders, const vector<Point>& route) : dist_sum(0), orders(orders), route(route) {
        for (size_t i = 0; i < route.size() - 1; ++i) {
            dist_sum += route[i].dist(route[i + 1]);
        }
    }

    void print_output() const {
        cout << orders.size() << " ";
        for (size_t i = 0; i < orders.size(); ++i) {
            if (i > 0) cout << " ";
            cout << orders[i] + 1;
        }
        cout << endl;

        cout << route.size();
        for (const auto& p : route) {
            cout << " " << p.x << " " << p.y;
        }
        cout << endl;
    }
};

// solve_greedy関数
Output solve_greedy(const Input& input_data, const vector<int>& selected_orders) {
    const vector<Point>& restaurants = input_data.restaurants;
    const vector<Point>& destinations = input_data.destinations;
    vector<Point> route;
    Point current_position(400, 400);
    set<Point*> visitables;

    for (int i : selected_orders) {
        visitables.insert(new Restaurant(restaurants[i].x, restaurants[i].y, i));
    }

    route.push_back(current_position);

    while (!visitables.empty()) {
        int min_dist = INT_MAX;
        Point* next_position = nullptr;

        for (const auto& visitable : visitables) {
            int dist = current_position.dist(*visitable);
            if (dist < min_dist) {
                min_dist = dist;
                next_position = visitable;
            }
        }

        route.push_back(*next_position);

        if (auto* restaurant = dynamic_cast<Restaurant*>(next_position)) {
            int idx = restaurant->idx;
            visitables.insert(new Destination(destinations[idx].x, destinations[idx].y, idx));
        }

        visitables.erase(next_position);
        delete next_position; // メモリ解放
        current_position = route.back();
    }

    route.push_back(Point(400, 400));

    return Output(selected_orders, route);
}

// is_valid_order関数
bool is_valid_order(const vector<Point>& route) {
    set<int> got_restaurants;

    for (const auto& point : route) {
        if (const auto* restaurant = dynamic_cast<const Restaurant*>(&point)) {
            got_restaurants.insert(restaurant->idx);
        } else if (const auto* destination = dynamic_cast<const Destination*>(&point)) {
            if (got_restaurants.find(destination->idx) == got_restaurants.end()) {
                return false;
            }
        }
    }

    return true;
}

// get_distance関数
int get_distance(const vector<Point>& route) {
    int dist = 0;

    for (size_t i = 0; i < route.size() - 1; ++i) {
        dist += route[i].dist(route[i + 1]);
    }

    return dist;
}

// solve_efficient_annealing関数
Output solve_efficient_annealing(const Input& input_data, const Output& output_data_greedy) {
    set<int> current_orders(output_data_greedy.orders.begin(), output_data_greedy.orders.end());
    vector<Point> current_route = output_data_greedy.route;
    int current_dist = get_distance(current_route);

    vector<int> best_orders(current_orders.begin(), current_orders.end());
    vector<Point> best_route = current_route;
    int best_dist = current_dist;

    double start_temperature = 50.0;
    double end_temperature = 1.0;
    double current_temperature = start_temperature;

    double time_limit = 1.5;
    auto start_time = high_resolution_clock::now();

    mt19937 rng(42);
    uniform_real_distribution<double> random_double(0.0, 1.0);

    int iteration = 0;

    while (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() < time_limit * 1000) {
        int remove_order = *next(current_orders.begin(), rng() % current_orders.size());
        int add_order = candidates[rng() % candidates.size()];

        while (current_orders.count(add_order)) {
            add_order = candidates[rng() % candidates.size()];
        }

        set<int> new_orders = current_orders;
        new_orders.erase(remove_order);
        new_orders.insert(add_order);

        Output output = solve_greedy(input_data, vector<int>(new_orders.begin(), new_orders.end()));
        int new_dist = get_distance(output.route);

        if (new_dist <= current_dist || random_double(rng) <= exp((current_dist - new_dist) / current_temperature)) {
            current_orders = new_orders;
            current_route = output.route;
            current_dist = new_dist;

            if (current_dist < best_dist) {
                best_dist = current_dist;
                best_route = current_route;
                best_orders = vector<int>(current_orders.begin(), current_orders.end());
            }
        }

        double progress = duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() / (time_limit * 1000.0);
        current_temperature = pow(start_temperature, 1.0 - progress) * pow(end_temperature, progress);

        iteration++;
    }

    return Output(best_orders, best_route);
}

// update_distance関数のプロトタイプ宣言を追加
int update_distance(const vector<Point>& route, int i, int j);

// solve_simulated_annealing関数の未使用引数を削除
Output solve_simulated_annealing(const Input&, const Output& output_data_greedy) {
    vector<int> orders = output_data_greedy.orders;
    vector<Point> route = output_data_greedy.route;
    int current_dist = get_distance(route);

    vector<int> best_orders = orders;
    vector<Point> best_route = route;
    int best_dist = current_dist;

    mt19937 rng(42);
    uniform_real_distribution<double> random_double(0.0, 1.0);

    double start_temperature = 10.0;
    double end_temperature = 1.0;
    double current_temperature = start_temperature;

    double time_limit = 1.78;
    auto start_time = high_resolution_clock::now();

    int iteration = 0;

    while (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() < time_limit * 1000) {
        int i = rng() % route.size();
        int j = rng() % route.size();

        int delta = update_distance(route, i, j); // 修正: update_distance関数が見つかるように修正
        if (delta <= 0 || random_double(rng) < exp(-delta / current_temperature)) {
            swap(route[i], route[j]);
            current_dist += delta;

            if (current_dist < best_dist) {
                best_dist = current_dist;
                best_route = route;
                best_orders = orders;
            }
        }

        double progress = duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() / (time_limit * 1000.0);
        current_temperature = pow(start_temperature, 1.0 - progress) * pow(end_temperature, progress);

        iteration++;
    }

    return Output(best_orders, best_route);
}

// update_distance関数
int update_distance(const vector<Point>& route, int i, int j) {
    if (i == j) {
        return 0;
    } else if (i > j) {
        int before = route[j].dist(route[j - 1]) + route[i].dist(route[i - 1]) + route[i + 1].dist(route[i]);
        int after = route[i].dist(route[j]) + route[i].dist(route[j - 1]) + route[i - 1].dist(route[i + 1]);
        return after - before;
    } else {
        int before = route[j + 1].dist(route[j]) + route[i].dist(route[i - 1]) + route[i + 1].dist(route[i]);
        int after = route[j + 1].dist(route[i]) + route[j].dist(route[i]) + route[i + 1].dist(route[i - 1]);
        return after - before;
    }
}

int main() {
    auto start_time = high_resolution_clock::now();

    Input input_data = Input::read();

    vector<int> sorted_orders(input_data.order_count);
    iota(sorted_orders.begin(), sorted_orders.end(), 0);

    sort(sorted_orders.begin(), sorted_orders.end(), [&](int i, int j) {
        int dist_i = max(
            Point(400, 400).dist(input_data.restaurants[i]),
            Point(400, 400).dist(input_data.destinations[i])
        );
        int dist_j = max(
            Point(400, 400).dist(input_data.restaurants[j]),
            Point(400, 400).dist(input_data.destinations[j])
        );
        return dist_i < dist_j;
    });

    for (int i = 0; i < input_data.order_count; ++i) {
        if (input_data.office.dist(input_data.restaurants[i]) <= 350 &&
            input_data.office.dist(input_data.destinations[i]) <= 350) {
            candidates.push_back(i);
        }
    }

    vector<int> first_selected_orders(sorted_orders.begin(), sorted_orders.begin() + input_data.pickup_count);

    Output output_data_greedy = solve_greedy(input_data, first_selected_orders);

    Output output_data_sa = solve_efficient_annealing(input_data, output_data_greedy);

    Output output_data = solve_simulated_annealing(input_data, output_data_sa);

    output_data.print_output();

    auto end_time = high_resolution_clock::now();
    cerr << "Execution time: "
         << duration_cast<milliseconds>(end_time - start_time).count()
         << " ms" << endl;

    return 0;
}
