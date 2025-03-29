use std::collections::{HashSet, HashMap};
use std::time::{Duration, Instant};
use rand::prelude::*;
use std::io;

// 定数
const PRIME_NUMBER: i64 = 998_244_353;
const BASE: i64 = 10_007;
const OFFICE_X: i32 = 400;
const OFFICE_Y: i32 = 400;

// ハッシュ関数
fn get_hash(x: i32, y: i32, idx: usize, tp: i32) -> i64 {
    let base64 = BASE as i64;
    let x64 = x as i64;
    let y64 = y as i64;
    let idx64 = idx as i64;
    let tp64 = tp as i64;

    (x64 + y64 * base64 + 
     idx64 * base64.pow(2) + 
     tp64 * base64.pow(3)) % PRIME_NUMBER
}

// 点の構造体
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Point { x, y }
    }

    // マンハッタン距離の計算
    fn dist(&self, other: &Point) -> i32 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

// レストランの構造体
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Restaurant {
    point: Point,
    idx: usize,
}

impl Restaurant {
    fn new(x: i32, y: i32, idx: usize) -> Self {
        Restaurant { 
            point: Point::new(x, y), 
            idx 
        }
    }
}

// 目的地の構造体
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Destination {
    point: Point,
    idx: usize,
}

impl Destination {
    fn new(x: i32, y: i32, idx: usize) -> Self {
        Destination { 
            point: Point::new(x, y), 
            idx 
        }
    }
}

// 入力データの構造体
#[derive(Debug, Clone)]
struct Input {
    order_count: usize,
    pickup_count: usize,
    office: Point,
    restaurants: Vec<Point>,
    destinations: Vec<Point>,
}

impl Input {
    // 入力データの読み込み
    fn read() -> io::Result<Self> {
        let order_count = 1000;
        let pickup_count = 50;
        let office = Point::new(OFFICE_X, OFFICE_Y);
        let mut restaurants = Vec::new();
        let mut destinations = Vec::new();

        for _ in 0..order_count {
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line)?;
            let parts: Vec<i32> = input_line
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            
            restaurants.push(Point::new(parts[0], parts[1]));
            destinations.push(Point::new(parts[2], parts[3]));
        }

        Ok(Input {
            order_count,
            pickup_count,
            office,
            restaurants,
            destinations,
        })
    }
}

// 出力データの構造体
#[derive(Debug, Clone)]
struct Output {
    dist_sum: i32,
    orders: Vec<usize>,
    route: Vec<RoutePoint>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum RoutePoint {
    Office(Point),
    RestaurantPoint(Restaurant),
    DestinationPoint(Destination),
}

impl Output {
    fn new(orders: Vec<usize>, route: Vec<RoutePoint>) -> Self {
        let dist_sum = route.windows(2)
            .map(|window| match (window[0], window[1]) {
                (RoutePoint::Office(p1), RoutePoint::Office(p2)) => p1.dist(&p2),
                (RoutePoint::Office(p1), RoutePoint::RestaurantPoint(r2)) => p1.dist(&r2.point),
                (RoutePoint::Office(p1), RoutePoint::DestinationPoint(d2)) => p1.dist(&d2.point),
                (RoutePoint::RestaurantPoint(r1), RoutePoint::Office(p2)) => r1.point.dist(&p2),
                (RoutePoint::RestaurantPoint(r1), RoutePoint::RestaurantPoint(r2)) => r1.point.dist(&r2.point),
                (RoutePoint::RestaurantPoint(r1), RoutePoint::DestinationPoint(d2)) => r1.point.dist(&d2.point),
                (RoutePoint::DestinationPoint(d1), RoutePoint::Office(p2)) => d1.point.dist(&p2),
                (RoutePoint::DestinationPoint(d1), RoutePoint::RestaurantPoint(r2)) => d1.point.dist(&r2.point),
                (RoutePoint::DestinationPoint(d1), RoutePoint::DestinationPoint(d2)) => d1.point.dist(&d2.point),
            })
            .sum();

        Output {
            dist_sum,
            orders,
            route,
        }
    }

    // 解の出力
    fn print_output(&self) {
        // 選択した注文の出力
        print!("{} ", self.orders.len());
        let formatted_orders: Vec<String> = self.orders.iter().map(|&x| (x + 1).to_string()).collect();
        println!("{}", formatted_orders.join(" "));

        // 配達ルートの出力
        print!("{}", self.route.len());
        for point in &self.route {
            match point {
                RoutePoint::Office(p) | 
                RoutePoint::RestaurantPoint(Restaurant { point: p, .. }) | 
                RoutePoint::DestinationPoint(Destination { point: p, .. }) => {
                    print!(" {} {}", p.x, p.y);
                }
            }
        }
        println!();
    }
}

// 貪欲法のソルバー
fn solve_greedy(input: &Input, selected_orders: &[usize]) -> Output {
    let mut route = vec![RoutePoint::Office(input.office)];
    let mut current_position = input.office;
    let mut visitables: HashSet<_> = selected_orders
        .iter()
        .map(|&i| RoutePoint::RestaurantPoint(Restaurant::new(
            input.restaurants[i].x, 
            input.restaurants[i].y, 
            i
        )))
        .collect();

    while !visitables.is_empty() {
        let next_position = visitables
            .iter()
            .min_by_key(|&visitable| {
                let point = match visitable {
                    RoutePoint::RestaurantPoint(r) => r.point,
                    RoutePoint::DestinationPoint(d) => d.point,
                    _ => unreachable!(),
                };
                current_position.dist(&point)
            })
            .cloned()
            .unwrap();

        route.push(next_position);

        match next_position {
            RoutePoint::RestaurantPoint(restaurant) => {
                visitables.insert(RoutePoint::DestinationPoint(Destination::new(
                    input.destinations[restaurant.idx].x,
                    input.destinations[restaurant.idx].y,
                    restaurant.idx,
                )));
            }
            _ => {}
        }

        visitables.remove(&next_position);
        current_position = match next_position {
            RoutePoint::RestaurantPoint(r) => r.point,
            RoutePoint::DestinationPoint(d) => d.point,
            _ => unreachable!(),
        };
    }

    route.push(RoutePoint::Office(input.office));
    Output::new(selected_orders.to_vec(), route)
}

// 距離計算関数
fn get_distance(route: &[RoutePoint]) -> i32 {
    route.windows(2)
        .map(|window| match (window[0], window[1]) {
            (RoutePoint::Office(p1), RoutePoint::Office(p2)) => p1.dist(&p2),
            (RoutePoint::Office(p1), RoutePoint::RestaurantPoint(r2)) => p1.dist(&r2.point),
            (RoutePoint::Office(p1), RoutePoint::DestinationPoint(d2)) => p1.dist(&d2.point),
            (RoutePoint::RestaurantPoint(r1), RoutePoint::Office(p2)) => r1.point.dist(&p2),
            (RoutePoint::RestaurantPoint(r1), RoutePoint::RestaurantPoint(r2)) => r1.point.dist(&r2.point),
            (RoutePoint::RestaurantPoint(r1), RoutePoint::DestinationPoint(d2)) => r1.point.dist(&d2.point),
            (RoutePoint::DestinationPoint(d1), RoutePoint::Office(p2)) => d1.point.dist(&p2),
            (RoutePoint::DestinationPoint(d1), RoutePoint::RestaurantPoint(r2)) => d1.point.dist(&r2.point),
            (RoutePoint::DestinationPoint(d1), RoutePoint::DestinationPoint(d2)) => d1.point.dist(&d2.point),
        })
        .sum()
}

// 経路の有効性チェック関数
fn is_valid_order(route: &[RoutePoint]) -> bool {
    let mut got_restaurants = HashSet::new();
    
    for point in route {
        match point {
            RoutePoint::RestaurantPoint(r) => {
                got_restaurants.insert(r.idx);
            },
            RoutePoint::DestinationPoint(d) => {
                if !got_restaurants.contains(&d.idx) {
                    return false;
                }
            },
            _ => {}
        }
    }
    true
}

// インデックス更新関数
fn update_index(
    destination_dict: &mut HashMap<usize, usize>, 
    restaurant_dict: &mut HashMap<usize, usize>, 
    i: usize, 
    j: usize
) {
    if i < j {
        for value in destination_dict.values_mut() {
            if *value > i && *value <= j {
                *value -= 1;
            }
        }
        for value in restaurant_dict.values_mut() {
            if *value > i && *value <= j {
                *value -= 1;
            }
        }
    } else if i > j {
        for value in destination_dict.values_mut() {
            if *value < i && *value >= j {
                *value += 1;
            }
        }
        for value in restaurant_dict.values_mut() {
            if *value < i && *value >= j {
                *value += 1;
            }
        }
    }
}

// 距離更新関数
fn update_distance(route: &[RoutePoint], i: usize, j: usize) -> i32 {
    if i == j {
        return 0;
    }
    
    let mut test_route = route.to_vec();
    let point_to_move = test_route.remove(i);
    test_route.insert(j, point_to_move);
    
    get_distance(&test_route) - get_distance(route)
}

// 効率的な焼きなまし法
fn solve_efficient_annealing(input: &Input, output_data_greedy: &Output, candidates: &[usize]) -> Output {
    let mut rng = StdRng::seed_from_u64(42);
    let start_time = Instant::now();
    let time_limit = Duration::from_secs_f64(1.5);

    let mut current_orders = output_data_greedy.orders.clone();
    let mut current_route = output_data_greedy.route.clone();
    let mut current_dist = get_distance(&current_route);

    let mut best_orders = current_orders.clone();
    let mut best_route = current_route.clone();
    let mut best_dist = current_dist;

    let start_temperature: f64 = 70.0;
    let end_temperature: f64 = 5.0;

    let mut current_temperature = start_temperature;
    let mut iteration = 0;

    while start_time.elapsed() < time_limit {
        // ランダムに削除する注文と追加する注文を選択
        let remove_order = current_orders[rng.gen_range(0..current_orders.len())];
        let mut add_order = candidates[rng.gen_range(0..candidates.len())];

        while current_orders.contains(&add_order) {
            add_order = candidates[rng.gen_range(0..candidates.len())];
        }

        // 新しい注文セットの作成
        let mut new_orders = current_orders.clone();
        new_orders.retain(|&x| x != remove_order);
        new_orders.push(add_order);

        // 新しい経路の生成と距離計算
        let output = solve_greedy(input, &new_orders);
        let new_dist = get_distance(&output.route);

        // 受理基準
        let accept_prob = if new_dist <= current_dist {
            1.0
        } else {
            (-((new_dist - current_dist) as f64) / current_temperature).exp()
        };

        if accept_prob > rng.gen() {
            current_orders = new_orders;
            current_route = output.route;
            current_dist = new_dist;

            // 最良解の更新
            if current_dist < best_dist {
                best_dist = current_dist;
                best_route = current_route.clone();
                best_orders = current_orders.clone();
            }
        }

        // 温度更新
        let progress = start_time.elapsed().as_secs_f64() / time_limit.as_secs_f64();
        current_temperature = start_temperature.powf(1.0 - progress) * end_temperature.powf(progress);

        iteration += 1;
        if iteration % 1000 == 0 {
            eprintln!("iteration: {}, total distance: {}", iteration, current_dist);
        }
    }

    eprintln!("--- Result ---");
    eprintln!("iteration: {}", iteration);
    eprintln!("total distance: {}", best_dist);

    Output::new(best_orders, best_route)
}

// シミュレーテッドアニーリング法
fn solve_simulated_annealing(input: &Input, output_data_greedy: &Output) -> Output {
    let mut rng = StdRng::seed_from_u64(42);
    let start_time = Instant::now();
    let time_limit = Duration::from_secs_f64(0.49); 

    let mut orders = output_data_greedy.orders.clone();
    let mut route = output_data_greedy.route.clone();

    let mut current_dist = get_distance(&route);

    let mut best_orders = orders.clone();
    let mut best_route = route.clone();
    let mut best_dist = current_dist;

    let start_temperature: f64 = 10.0;
    let end_temperature: f64 = 1.0;

    let mut current_temperature = start_temperature;

    // レストランと配達先のルート中のインデックスの辞書
    let mut restaurant_dict: HashMap<usize, usize> = orders
        .iter()
        .map(|&order| {
            (order, route.iter().position(|&r| 
                matches!(r, RoutePoint::RestaurantPoint(rest) if rest.idx == order)
            ).unwrap())
        })
        .collect();

    let mut destination_dict: HashMap<usize, usize> = orders
        .iter()
        .map(|&order| {
            (order, route.iter().position(|&d| 
                matches!(d, RoutePoint::DestinationPoint(dest) if dest.idx == order)
            ).unwrap())
        })
        .collect();

    let mut iteration = 0;

    while start_time.elapsed() < time_limit {
        let rand_order = orders[rng.gen_range(0..orders.len())];

        if iteration % 2 == 0 {
            // レストランを選んで配達先よりも前に挿入
            let i = restaurant_dict[&rand_order];
            let j = rng.gen_range(1..destination_dict[&rand_order]);
            
            let delta = update_distance(&route, i, j);
            
            let accept_prob = if delta <= 0 {
                1.0
            } else {
                (-delta as f64 / current_temperature).exp()
            };

            if accept_prob > rng.gen() {
                update_index(&mut destination_dict, &mut restaurant_dict, i, j);
                restaurant_dict.insert(rand_order, j);
                
                let point_to_move = route.remove(i);
                route.insert(j, point_to_move);
                
                current_dist += delta;
                
                if current_dist < best_dist {
                    best_route = route.clone();
                    best_dist = current_dist;
                }
            }
        } else {
            // 配達先を選んでレストランよりも後に挿入
            let i = destination_dict[&rand_order];
            let j = rng.gen_range(
                restaurant_dict[&rand_order] + 1..
                2 * input.pickup_count
            );
            
            let delta = update_distance(&route, i, j);
            
            let accept_prob = if delta <= 0 {
                1.0
            } else {
                (-delta as f64 / current_temperature).exp()
            };

            if accept_prob > rng.gen() {
                update_index(&mut destination_dict, &mut restaurant_dict, i, j);
                destination_dict.insert(rand_order, j);
                
                let point_to_move = route.remove(i);
                route.insert(j, point_to_move);
                
                current_dist += delta;
                
                if current_dist < best_dist {
                    best_route = route.clone();
                    best_dist = current_dist;
                }
            }
        }

        iteration += 1;
        if iteration % 100000 == 0 {
            eprintln!("iteration: {}, total distance: {}", iteration, current_dist);
        }

        // 温度更新
        let progress = start_time.elapsed().as_secs_f64() / time_limit.as_secs_f64();
        current_temperature = start_temperature.powf(1.0 - progress) * end_temperature.powf(progress);
    }

    eprintln!("--- Result ---");
    eprintln!("iteration     : {}", iteration);
    eprintln!("total distance: {}", best_dist);

    Output::new(best_orders, best_route)
}

fn main() -> io::Result<()> {
    let input_data = Input::read()?;
    
    // 候補注文の選択
    let mut candidates = Vec::new();
    for i in 0..input_data.order_count {
        if input_data.office.dist(&input_data.restaurants[i]) <= 400 && 
           input_data.office.dist(&input_data.destinations[i]) <= 400 {
            candidates.push(i);
        }
    }

    // 初期注文の選択（コストが小さい順）
    let mut sorted_orders: Vec<usize> = (0..input_data.order_count).collect();
    sorted_orders.sort_by_key(|&i| 
        std::cmp::max(
            input_data.office.dist(&input_data.restaurants[i]),
            input_data.office.dist(&input_data.destinations[i])
        )
    );

    let first_selected_orders = &sorted_orders[..input_data.pickup_count];
    let output_data_greedy = solve_greedy(&input_data, first_selected_orders);
    let output_data_ea = solve_efficient_annealing(&input_data, &output_data_greedy, &candidates);
    let output_data_sa = solve_simulated_annealing(&input_data, &output_data_ea);
    output_data_sa.print_output();

    Ok(())
}