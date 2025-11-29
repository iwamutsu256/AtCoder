import sys
import math
import heapq
import random
import time

# --- 定数設定 ---
# 全体の制限時間 (秒)
TOTAL_TIME_LIMIT = 1.8

# 成長フェーズ数: サイズ1 -> 30 まで、1つずつ増やすので29回
NUM_GROWTH_PHASES = 29 

# 時間ペナルティ係数
# 距離(二乗)と時間のトレードオフ。早く結合することを優先させるための重み。
TIME_PENALTY = 10.0

# 孤立原子回収ボーナスの重み
# この値が大きいほど、「遠くにある原子(孤立原子)」を優先的に拾いに行きます
ISOLATION_WEIGHT = 0.8

# Core選定時の山登り回数
CORE_HC_ITERATIONS = 1500

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
    
    Returns: (min_d2, dt)  dtはstart_tからの経過時間
    """
    duration = end_t - start_t
    if duration < 0: return float('inf'), 0

    min_d2 = float('inf')
    best_dt = 0
    
    A = vx**2 + vy**2

    # 相対速度0（平行移動）の場合
    if A == 0:
        d2 = calc_torus_dist_sq(sx, sy, tx, ty, L)
        return d2, 0

    # トーラス環境を考慮し、ターゲット点を周囲9方向に展開して計算
    offsets = [-L, 0, L]
    
    for dx_offset in offsets:
        for dy_offset in offsets:
            target_x = tx + dx_offset
            target_y = ty + dy_offset
            
            dx = sx - target_x
            dy = sy - target_y
            
            # 距離の二乗 f(t) = A*t^2 + B*t + C
            B = 2 * (vx * dx + vy * dy)
            C = dx**2 + dy**2
            
            # 極値 t = -B / (2A)
            t_extremum = -B / (2 * A)
            
            # 探索範囲: [0, duration]
            candidates = [0, duration]
            if 0 < t_extremum < duration:
                candidates.append(t_extremum)
            
            for dt in candidates:
                dist_sq = A * (dt**2) + B * dt + C
                if dist_sq < min_d2:
                    min_d2 = dist_sq
                    best_dt = dt
                    
    return min_d2, best_dt

# --- クラス定義 ---

class Atom:
    """原子の状態を管理するクラス"""
    def __init__(self, aid, x, y, vx, vy, t_update):
        self.id = aid
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.t_update = float(t_update)

    def get_pos_at(self, t, L):
        """指定時刻 t における位置を返す"""
        if t <= self.t_update:
            return self.x, self.y
        dt = t - self.t_update
        nx = (self.x + self.vx * dt) % L
        ny = (self.y + self.vy * dt) % L
        return nx, ny
    
    def update(self, t, nx, ny, nvx, nvy):
        """状態を更新する"""
        self.x = nx
        self.y = ny
        self.vx = nvx
        self.vy = nvy
        self.t_update = t

class Component:
    """連結成分（分子）を管理するクラス"""
    def __init__(self, c_id, atom_indices):
        self.id = c_id
        self.atom_indices = atom_indices # list of atom IDs
        self.valid = True
    
    def size(self):
        return len(self.atom_indices)

# --- メインソルバー ---

def solve():
    # 入力読み込み
    input = sys.stdin.readline
    try:
        line1 = input().split()
        if not line1: return
        N, T, M, K, L = map(int, line1)
    except ValueError:
        return

    # 原子管理用オブジェクト作成
    atom_objects = []
    for i in range(N):
        x, y, vx, vy = map(int, input().split())
        atom_objects.append(Atom(i, x, y, vx, vy, 0))

    # 全原子を初期コンポーネント化
    all_components = []
    for i in range(N):
        c = Component(i, [i])
        all_components.append(c)

    # ---------------------------------------------------------
    # Step 1: Core（核）の選定 (山登り法)
    # ---------------------------------------------------------
    # 「分散していて」かつ「近傍の密度が高い」原子セットを選ぶ
    
    # 1. 各原子の「局所密度スコア」を計算（近傍k個との距離二乗和）
    local_sparsity = []
    k_neighbors = 5
    
    for i in range(N):
        dists = []
        c_atom = atom_objects[i]
        cx, cy = c_atom.get_pos_at(0, L)
        for j in range(N):
            if i == j: continue
            t_atom = atom_objects[j]
            tx, ty = t_atom.get_pos_at(0, L)
            d2 = calc_torus_dist_sq(cx, cy, tx, ty, L)
            dists.append(d2)
        dists.sort()
        # 近いk個の距離和を「疎度」とする（小さいほど密）
        sparsity = sum(dists[:k_neighbors])
        local_sparsity.append(sparsity)

    random.seed(42)
    
    # 評価関数: 分散(最大化) - 重み * 密度(最小化) => 全体を最小化
    # ※ここではスコアを最小化する方向で定義する
    # Score = (密度の総和) - Weight * (Core間最小距離)
    def calculate_core_set_score(core_indices):
        min_inter_core_dist = float('inf')
        # Core間の最小距離を計算
        for i in range(M):
            for j in range(i+1, M):
                idx1 = core_indices[i]
                idx2 = core_indices[j]
                a1 = atom_objects[idx1]
                a2 = atom_objects[idx2]
                d2 = calc_torus_dist_sq(a1.x, a1.y, a2.x, a2.y, L)
                if d2 < min_inter_core_dist:
                    min_inter_core_dist = d2
        
        total_sparsity = sum(local_sparsity[idx] for idx in core_indices)
        
        # 重み付け: 分散（最小距離）を大きく保つことを重視
        return total_sparsity - 2.0 * min_inter_core_dist

    # 初期解: ランダム
    current_cores_indices = random.sample(range(N), M)
    current_score = calculate_core_set_score(current_cores_indices)
    
    # 山登り法
    for _ in range(CORE_HC_ITERATIONS):
        # 1つ入れ替え
        remove_pos = random.randint(0, M-1)
        
        # 新しい候補 (現在のCoreに含まれないもの)
        while True:
            new_cand = random.randint(0, N-1)
            if new_cand not in current_cores_indices:
                break
        
        # 仮更新
        old_val = current_cores_indices[remove_pos]
        current_cores_indices[remove_pos] = new_cand
        
        new_score = calculate_core_set_score(current_cores_indices)
        
        if new_score < current_score:
            # 採用
            current_score = new_score
        else:
            # 棄却 (元に戻す)
            current_cores_indices[remove_pos] = old_val

    # 確定したCoreを設定
    is_core = [False] * N
    cores = []
    for idx in current_cores_indices:
        is_core[idx] = True
        cores.append(all_components[idx])

    # 残りはFreeリストへ
    frees = [all_components[i] for i in range(N) if not is_core[i]]

    operations = []
    start_time = time.time()

    # ---------------------------------------------------------
    # Step 2: フェーズ時間割の計算 (指数増加)
    # ---------------------------------------------------------
    # 後半の比重を重くする。指数的に増加させる。
    # 1.1^0 = 1, ..., 1.1^28 ≈ 14.4
    weights = [1.1 ** i for i in range(NUM_GROWTH_PHASES)]
    total_weight = sum(weights)
    
    available_time_for_search = TOTAL_TIME_LIMIT - 0.1
    phase_time_budgets = [available_time_for_search * (w / total_weight) for w in weights]
    
    phase_end_times = []
    current_end = 0.0
    for w in weights:
        duration = T * (w / total_weight)
        current_end += duration
        phase_end_times.append(current_end)
    
    # 最終ターンは確実にT
    phase_end_times[-1] = T

    # ---------------------------------------------------------
    # Step 3: 成長フェーズループ (29回)
    # ---------------------------------------------------------
    for phase in range(NUM_GROWTH_PHASES):
        phase_start_time = time.time()
        current_time_budget = phase_time_budgets[phase]
        
        phase_end_t = phase_end_times[phase]
        search_limit_t = min(T, phase_end_t + 50) 
        
        num_cores = len(cores)
        num_frees = len(frees)
        
        # --- 孤立度(Isolation Score)の計算 ---
        # 各Free原子について、「現在最も近いCoreとの距離」を計算
        isolation_scores = {}
        
        # 基準時刻: Coreの平均的な現在時刻
        base_t = sum(atom_objects[c.atom_indices[0]].t_update for c in cores) / num_cores
        
        for f_idx, free in enumerate(frees):
            free_atom = atom_objects[free.atom_indices[0]]
            fx, fy = free_atom.get_pos_at(base_t, L)
            
            min_dist_to_any_core = float('inf')
            
            # サンプリングでCoreとの距離を測る
            for core in cores:
                core_rep = atom_objects[core.atom_indices[0]]
                cx, cy = core_rep.get_pos_at(base_t, L)
                d2 = calc_torus_dist_sq(cx, cy, fx, fy, L)
                if d2 < min_dist_to_any_core:
                    min_dist_to_any_core = d2
            
            isolation_scores[f_idx] = min_dist_to_any_core

        # --- 初期解生成 (Weighted Greedy) ---
        used_free_mask = [False] * num_frees
        assignment = [-1] * num_cores 
        
        for i in range(num_cores):
            core = cores[i]
            best_f_idx = -1
            min_eval_score = float('inf')
            
            search_indices = random.sample(range(num_frees), min(num_frees, 30))
            core_atoms = [atom_objects[aid] for aid in core.atom_indices]
            
            for f_idx in search_indices:
                if used_free_mask[f_idx]: continue
                free = frees[f_idx]
                free_atom = atom_objects[free.atom_indices[0]] 
                
                base_t = core_atoms[0].t_update
                fx, fy = free_atom.get_pos_at(base_t, L)
                
                # Core内原子との最短距離
                min_d2_local = float('inf')
                for ca in core_atoms:
                    cx, cy = ca.get_pos_at(base_t, L)
                    d2 = calc_torus_dist_sq(cx, cy, fx, fy, L)
                    if d2 < min_d2_local:
                        min_d2_local = d2
                
                # 評価値 = 距離 - ボーナス
                eval_score = min_d2_local - ISOLATION_WEIGHT * isolation_scores[f_idx]
                
                if eval_score < min_eval_score:
                    min_eval_score = eval_score
                    best_f_idx = f_idx
            
            if best_f_idx == -1:
                for k in range(num_frees):
                    if not used_free_mask[k]:
                        best_f_idx = k
                        break
            
            assignment[i] = best_f_idx
            used_free_mask[best_f_idx] = True

        # --- 評価関数 ---
        eval_cache = {}

        def get_eval_info(c_idx, f_idx):
            key = (c_idx, f_idx)
            if key in eval_cache: return eval_cache[key]
            
            core = cores[c_idx]
            free = frees[f_idx]
            free_atom = atom_objects[free.atom_indices[0]]
            core_atoms = [atom_objects[aid] for aid in core.atom_indices]
            
            start_search_t = max(core_atoms[0].t_update, free_atom.t_update)
            
            if start_search_t >= search_limit_t:
                return float('inf'), T, -1
            
            best_min_d2 = float('inf')
            best_dt = 0
            best_atom_id = -1
            
            # Core内の全原子とFree原子のペアで最接近を探す
            for ca in core_atoms:
                dvx = ca.vx - free_atom.vx
                dvy = ca.vy - free_atom.vy
                px, py = ca.get_pos_at(start_search_t, L)
                qx, qy = free_atom.get_pos_at(start_search_t, L)
                
                duration = max(0, search_limit_t - start_search_t)
                min_d2, dt = get_trajectory_min_dist(px, py, dvx, dvy, qx, qy, 0, duration, L)
                
                if min_d2 < best_min_d2:
                    best_min_d2 = min_d2
                    best_dt = dt
                    best_atom_id = ca.id
            
            meet_t = start_search_t + best_dt
            
            # 純粋な軌道コスト + 時間ペナルティ
            raw_score = best_min_d2 + TIME_PENALTY * meet_t
            
            eval_cache[key] = (raw_score, meet_t, best_atom_id)
            return raw_score, meet_t, best_atom_id

        # 現在のスコア合計 (ボーナス込み)
        def calculate_total_score_with_bonus(current_assignment):
            total = 0
            for i in range(num_cores):
                f_idx = current_assignment[i]
                raw_score, _, _ = get_eval_info(i, f_idx)
                adjusted_score = raw_score - ISOLATION_WEIGHT * isolation_scores[f_idx]
                total += adjusted_score
            return total

        current_score = calculate_total_score_with_bonus(assignment)
        best_score = current_score
        best_assignment = list(assignment)
        
        # --- 焼きなまし (SA) ---
        start_temp = 50000.0
        end_temp = 100.0
        
        iter_count = 0
        while True:
            iter_count += 1
            if (iter_count & 31) == 0:
                if time.time() - phase_start_time > current_time_budget:
                    break
            
            elapsed = time.time() - phase_start_time
            progress = elapsed / current_time_budget
            current_temp = start_temp + (end_temp - start_temp) * progress
            
            type = random.randint(0, 1)
            
            if type == 0: # Swap
                c1 = random.randint(0, num_cores - 1)
                c2 = random.randint(0, num_cores - 1)
                if c1 == c2: continue
                
                f1 = assignment[c1]
                f2 = assignment[c2]
                
                raw1_old, _, _ = get_eval_info(c1, f1)
                raw2_old, _, _ = get_eval_info(c2, f2)
                raw1_new, _, _ = get_eval_info(c1, f2)
                raw2_new, _, _ = get_eval_info(c2, f1)
                
                # ボーナス項は入れ替わるだけなので合計不変
                delta = (raw1_new + raw2_new) - (raw1_old + raw2_old)
                
                if delta < 0 or random.random() < math.exp(-delta / current_temp):
                    assignment[c1] = f2
                    assignment[c2] = f1
                    current_score += delta
                    if current_score < best_score:
                        best_score = current_score
                        best_assignment = list(assignment)
                        
            else: # Change
                c1 = random.randint(0, num_cores - 1)
                f_old = assignment[c1]
                
                f_new = -1
                for _ in range(5):
                    r = random.randint(0, num_frees - 1)
                    if not used_free_mask[r]:
                        f_new = r
                        break
                if f_new == -1: continue
                
                raw_old, _, _ = get_eval_info(c1, f_old)
                raw_new, _, _ = get_eval_info(c1, f_new)
                
                score_old = raw_old - ISOLATION_WEIGHT * isolation_scores[f_old]
                score_new = raw_new - ISOLATION_WEIGHT * isolation_scores[f_new]
                
                delta = score_new - score_old
                
                if delta < 0 or random.random() < math.exp(-delta / current_temp):
                    assignment[c1] = f_new
                    used_free_mask[f_old] = False
                    used_free_mask[f_new] = True
                    current_score += delta
                    if current_score < best_score:
                        best_score = current_score
                        best_assignment = list(assignment)

        # --- 確定処理 ---
        next_frees = []
        assigned_frees_set = set(best_assignment)
        for i in range(num_frees):
            if i not in assigned_frees_set:
                next_frees.append(frees[i])
        
        for c_idx in range(num_cores):
            core = cores[c_idx]
            f_idx = best_assignment[c_idx]
            free = frees[f_idx]
            
            _, meet_t, best_atom_id = get_eval_info(c_idx, f_idx)
            
            # 時刻クランプ
            op_t = min(int(meet_t), T - 1)
            min_valid_t = 0
            for aid in core.atom_indices:
                min_valid_t = max(min_valid_t, atom_objects[aid].t_update)
            for aid in free.atom_indices:
                min_valid_t = max(min_valid_t, atom_objects[aid].t_update)
            
            op_t = max(op_t, int(min_valid_t))
            
            # 結合対象
            rep1 = best_atom_id
            if rep1 == -1: rep1 = core.atom_indices[0] 
            rep2 = free.atom_indices[0]
            
            operations.append((op_t, f"{op_t} {rep1} {rep2}"))
            
            # 新しい速度
            core_vx = atom_objects[core.atom_indices[0]].vx
            core_vy = atom_objects[core.atom_indices[0]].vy
            free_vx = atom_objects[rep2].vx
            free_vy = atom_objects[rep2].vy
            
            new_size = core.size() + 1
            new_vx = (core.size() * core_vx + 1 * free_vx) / new_size
            new_vy = (core.size() * core_vy + 1 * free_vy) / new_size
            
            # 原子更新
            for aid in core.atom_indices:
                a = atom_objects[aid]
                nx, ny = a.get_pos_at(op_t, L)
                a.update(op_t, nx, ny, new_vx, new_vy)
                
            fa = atom_objects[rep2]
            nx, ny = fa.get_pos_at(op_t, L)
            fa.update(op_t, nx, ny, new_vx, new_vy)
            
            core.atom_indices.append(rep2)
            
        frees = next_frees

    # 出力
    operations.sort(key=lambda x: x[0])
    for _, op_str in operations:
        print(op_str)

if __name__ == "__main__":
    solve()