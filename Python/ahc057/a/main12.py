import sys
import math
import heapq
import random
import time

# --- レシピ定義 ---
# 各フェーズで実施する結合の内容
# (フェーズ終了時刻, サイズ1, サイズ2, 作成ペア数)
RECIPES = [
    # Phase 1: 300個の1から、120組の(1+1=2)を作る。残りは60個の1。
    {"end_t": 150, "s1": 1, "s2": 1, "count": 120},
    # Phase 2: 120個の2と60個の1から、60組の(2+1=3)を作る。残りは60個の2。
    {"end_t": 300, "s1": 2, "s2": 1, "count": 60},
    # Phase 3: 60個の3と60個の2から、60組の(3+2=5)を作る。
    {"end_t": 450, "s1": 3, "s2": 2, "count": 60},
    # Phase 4: 60個の5から、30組の(5+5=10)を作る。
    {"end_t": 600, "s1": 5, "s2": 5, "count": 30},
    # Phase 5: 30個の10から、10組の(10+10=20)を作る。残りは10個の10。
    {"end_t": 800, "s1": 10, "s2": 10, "count": 10},
    # Phase 6: 10個の20と10個の10から、10組の(20+10=30)を作る。
    {"end_t": 1000, "s1": 20, "s2": 10, "count": 10},
]

# 全体の制限時間
TIME_LIMIT = 1.8

# --- 幾何計算関数 ---

def calc_torus_dist_sq(x1, y1, x2, y2, L):
    """
    トーラス環境下での2点間の距離の二乗を計算する。
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dist_x = min(dx, L - dx)
    dist_y = min(dy, L - dy)
    return dist_x**2 + dist_y**2

def get_trajectory_min_dist(sx, sy, vx, vy, tx, ty, start_t, end_t, L):
    """
    始点(sx,sy), 速度(vx,vy) の軌道と、点(tx,ty) との
    [start_t, end_t] の期間内の最小距離の二乗とその時の時刻を返す。
    ※(tx,ty)は静止していると仮定した相対計算を行う。
    (sx, sy) は 時刻 start_t における位置。
    """
    duration = end_t - start_t
    if duration < 0: return float('inf'), start_t

    min_d2 = float('inf')
    best_t = start_t
    
    A = vx**2 + vy**2

    if A == 0:
        d2 = calc_torus_dist_sq(sx, sy, tx, ty, L)
        return d2, start_t

    offsets = [-L, 0, L]
    
    for dx_offset in offsets:
        for dy_offset in offsets:
            target_x = tx + dx_offset
            target_y = ty + dy_offset
            
            dx = sx - target_x
            dy = sy - target_y
            
            B = 2 * (vx * dx + vy * dy)
            C = dx**2 + dy**2
            
            t_extremum = -B / (2 * A)
            
            candidates = [0, duration]
            if 0 < t_extremum < duration:
                candidates.append(t_extremum)
            
            for dt in candidates:
                dist_sq = A * (dt**2) + B * dt + C
                if dist_sq < min_d2:
                    min_d2 = dist_sq
                    best_t = start_t + dt
                    
    return min_d2, best_t

# --- クラス定義 ---

class Component:
    def __init__(self, c_id, atom_indices, x, y, vx, vy):
        self.id = c_id
        self.atom_indices = atom_indices 
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
    
    def size(self):
        return len(self.atom_indices)
    
    def update_position(self, dt, L):
        self.x = (self.x + self.vx * dt) % L
        self.y = (self.y + self.vy * dt) % L

# --- フェーズソルバー ---

def solve_phase(components, recipe, current_t, L, phase_time_limit):
    """
    1つのフェーズを実行する。
    greedy + swap hill climbing で最適なペアリングを見つける。
    """
    end_t = recipe["end_t"]
    s1 = recipe["s1"]
    s2 = recipe["s2"]
    count = recipe["count"]
    
    # 候補リスト作成
    group1 = [c for c in components if c.size() == s1]
    group2 = [c for c in components if c.size() == s2]
    
    # s1 == s2 の場合、group1とgroup2は同じオブジェクトを指す可能性があるため注意
    # 同じサイズ同士の結合の場合
    if s1 == s2:
        # group1 から 2*count 個選んでペアにする
        candidates = group1
        # IDでソートして再現性確保
        candidates.sort(key=lambda c: c.id)
    else:
        # 異なるサイズの場合
        # group1 (size s1) と group2 (size s2) は排反
        pass

    # --- ペアリングと最適化 ---
    # 結果として確定した (comp1, comp2, meet_t, cost) のリストを返す
    pairs = []
    
    # 距離計算キャッシュ: (id1, id2) -> (cost, dt)
    # フェーズ内では等速直線運動なので、一度計算すれば不変
    dist_cache = {}
    
    def get_dist_info(c1, c2):
        key = tuple(sorted((c1.id, c2.id)))
        if key in dist_cache:
            return dist_cache[key]
        
        # 軌道予測
        dvx = c1.vx - c2.vx
        dvy = c1.vy - c2.vy
        d2, dt = get_trajectory_min_dist(c1.x, c1.y, dvx, dvy, c2.x, c2.y, 0, end_t - current_t, L)
        dist_cache[key] = (d2, dt)
        return d2, dt

    # 初期解: 貪欲法
    # コストの小さいペアから順に確定させていく
    
    used_ids = set()
    
    if s1 == s2:
        # 同一プールからのマッチング
        pool = [c for c in candidates]
        # 全ペアのコストを計算してソートするのは重いかも (300*300/2 = 45000) -> 余裕
        edges = []
        for i in range(len(pool)):
            for j in range(i+1, len(pool)):
                d2, _ = get_dist_info(pool[i], pool[j])
                edges.append((d2, pool[i], pool[j]))
        
        edges.sort(key=lambda x: x[0])
        
        for d2, c1, c2 in edges:
            if len(pairs) >= count: break
            if c1.id in used_ids or c2.id in used_ids: continue
            
            used_ids.add(c1.id)
            used_ids.add(c2.id)
            _, dt = get_dist_info(c1, c2)
            pairs.append([c1, c2, dt, d2])
            
    else:
        # 異なるプール間のマッチング (Bipartite matching like)
        # group1 から count 個、group2 から count 個選ぶ
        # 貪欲: 全組み合わせ列挙してソート
        edges = []
        for c1 in group1:
            for c2 in group2:
                d2, _ = get_dist_info(c1, c2)
                edges.append((d2, c1, c2))
        
        edges.sort(key=lambda x: x[0])
        
        for d2, c1, c2 in edges:
            if len(pairs) >= count: break
            if c1.id in used_ids or c2.id in used_ids: continue
            
            used_ids.add(c1.id)
            used_ids.add(c2.id)
            _, dt = get_dist_info(c1, c2)
            pairs.append([c1, c2, dt, d2])

    # --- 山登り法 (Swap Optimization) ---
    # 時間が許す限りペアを交換してコストを下げる
    start_opt = time.time()
    
    while time.time() - start_opt < phase_time_limit:
        if len(pairs) < 2: break
        
        # ランダムに2つのペアを選ぶ
        idx_a = random.randint(0, len(pairs)-1)
        idx_b = random.randint(0, len(pairs)-1)
        if idx_a == idx_b: continue
        
        pair_a = pairs[idx_a] # [c1, c2, dt, cost]
        pair_b = pairs[idx_b]
        
        # Swapのパターン
        # Pair A: (A1, A2), Pair B: (B1, B2)
        # Swap 1: (A1, B2) & (B1, A2)
        # Swap 2: (A1, B1) & (A2, B2) -- サイズが違う場合は不可能な場合も
        
        # 今回のレシピでは、Pair内の [0]要素はサイズs1, [1]要素はサイズs2 となっているはず
        # 同サイズなら自由に交換可能、異サイズならs1同士・s2同士の交換のみ
        
        # Try swap: A1 <-> B1
        c_a1, c_a2 = pair_a[0], pair_a[1]
        c_b1, c_b2 = pair_b[0], pair_b[1]
        
        # Calculate new costs
        cost_new_a, dt_new_a = get_dist_info(c_b1, c_a2)
        cost_new_b, dt_new_b = get_dist_info(c_a1, c_b2)
        
        current_total = pair_a[3] + pair_b[3]
        new_total = cost_new_a + cost_new_b
        
        if new_total < current_total:
            # Swap A1, B1
            pair_a[0] = c_b1
            pair_a[2] = dt_new_a
            pair_a[3] = cost_new_a
            
            pair_b[0] = c_a1
            pair_b[2] = dt_new_b
            pair_b[3] = cost_new_b
            continue # Improvement found
            
        # Try swap: A2 <-> B2 (Same logic, effectively redundant if s1==s2 but useful)
        # If s1 != s2, we can swap A1<->B1 OR A2<->B2.
        
        cost_new_a2, dt_new_a2 = get_dist_info(c_a1, c_b2)
        cost_new_b2, dt_new_b2 = get_dist_info(c_b1, c_a2)
        
        new_total_2 = cost_new_a2 + cost_new_b2
        
        if new_total_2 < current_total:
            # Swap A2, B2
            pair_a[1] = c_b2
            pair_a[2] = dt_new_a2
            pair_a[3] = cost_new_a2
            
            pair_b[1] = c_a2
            pair_b[2] = dt_new_b2
            pair_b[3] = cost_new_b2
            
    # --- 結果の適用 ---
    ops_log = []
    next_components = []
    processed_ids = set()
    
    # 採用されたペアを処理
    for c1, c2, dt, _ in pairs:
        processed_ids.add(c1.id)
        processed_ids.add(c2.id)
        
        meet_t = current_t + dt
        meet_t = max(current_t, min(end_t - 1, meet_t))
        op_t = int(meet_t)
        
        rep1 = c1.atom_indices[0]
        rep2 = c2.atom_indices[0]
        ops_log.append(f"{op_t} {rep1} {rep2}")
        
        # 結合後の状態計算
        # 位置は結合時刻 op_t に合わせて進める
        dt_move = op_t - current_t
        c1.update_position(dt_move, L)
        c2.update_position(dt_move, L)
        
        # 合体位置 (c1基準)
        nx = c1.x # 実際は重心だが、仕様上どちらかの位置でよい
        ny = c1.y
        
        new_size = c1.size() + c2.size()
        new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
        new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
        
        # 新しいコンポーネント (IDは使わないので適当、位置は更新済み)
        # ただし、フェーズ終了までの残り時間を進める必要がある
        # ここでは「結合時刻」における状態を作成
        new_c = Component(-1, c1.atom_indices + c2.atom_indices, nx, ny, new_vx, new_vy)
        
        # フェーズ終了時刻まで進める
        remain_t = end_t - op_t
        new_c.update_position(remain_t, L)
        
        next_components.append(new_c)
        
    # ペアにならなかったコンポーネント
    for c in components:
        if c.id not in processed_ids:
            # フェーズ終了まで単独飛行
            c.update_position(end_t - current_t, L)
            next_components.append(c)
            
    # 次のフェーズ用にIDを振り直す（必須ではないがデバッグしやすい）
    for i, c in enumerate(next_components):
        c.id = i
        
    return next_components, ops_log

# --- メインソルバー ---

def solve():
    input = sys.stdin.readline
    try:
        line1 = input().split()
        if not line1: return
        N, T, M, K, L = map(int, line1)
    except ValueError:
        return

    atoms = []
    for i in range(N):
        x, y, vx, vy = map(int, input().split())
        atoms.append({
            'id': i, 'x': x, 'y': y, 'vx': vx, 'vy': vy
        })

    # 初期コンポーネント
    components = []
    for i in range(N):
        c = Component(i, [i], atoms[i]['x'], atoms[i]['y'], atoms[i]['vx'], atoms[i]['vy'])
        components.append(c)

    all_ops = []
    current_t = 0
    
    # 制限時間の配分
    # フェーズは6個。後半の数が減るので前半に時間を割きたいが、
    # 候補数が多い前半は計算時間がかかるので自然に配分される？
    # 均等割りで実装
    phase_time_budget = (TIME_LIMIT - 0.1) / len(RECIPES)

    for recipe in RECIPES:
        next_comps, ops = solve_phase(components, recipe, current_t, L, phase_time_budget)
        components = next_comps
        all_ops.extend(ops)
        current_t = recipe["end_t"]

    # 出力
    # 時刻順ソート
    parsed_ops = []
    for s in all_ops:
        t = int(s.split()[0])
        parsed_ops.append((t, s))
    
    parsed_ops.sort(key=lambda x: x[0])
    for _, s in parsed_ops:
        print(s)

if __name__ == "__main__":
    solve()