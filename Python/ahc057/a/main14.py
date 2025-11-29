import sys
import math
import heapq
import random
import time

# --- 定数 ---
TOTAL_TIME_LIMIT = 1.8
NUM_GROWTH_PHASES = 29 

# 時間ペナルティ係数
TIME_PENALTY = 10.0

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

    if A == 0:
        d2 = calc_torus_dist_sq(sx, sy, tx, ty, L)
        return d2, 0

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
    def __init__(self, aid, x, y, vx, vy, t_update):
        self.id = aid
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.t_update = float(t_update)

    def get_pos_at(self, t, L):
        if t <= self.t_update:
            return self.x, self.y
        dt = t - self.t_update
        nx = (self.x + self.vx * dt) % L
        ny = (self.y + self.vy * dt) % L
        return nx, ny
    
    def update(self, t, nx, ny, nvx, nvy):
        self.x = nx
        self.y = ny
        self.vx = nvx
        self.vy = nvy
        self.t_update = t

class Component:
    def __init__(self, c_id, atom_indices):
        self.id = c_id
        self.atom_indices = atom_indices # list of atom IDs
        self.valid = True
    
    def size(self):
        return len(self.atom_indices)

# --- メインソルバー ---

def solve():
    input = sys.stdin.readline
    try:
        line1 = input().split()
        if not line1: return
        N, T, M, K, L = map(int, line1)
    except ValueError:
        return

    # 原子管理用
    # Atomオブジェクトのリスト。インデックスがIDに対応。
    atom_objects = []
    for i in range(N):
        x, y, vx, vy = map(int, input().split())
        atom_objects.append(Atom(i, x, y, vx, vy, 0))

    # --- 初期化 ---
    # 全原子をコンポーネント化
    all_components = []
    for i in range(N):
        c = Component(i, [i])
        all_components.append(c)

# --- Core選定 ---
    # 分散していてかつ、近傍の密度が高い原子を選ぶ
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

    is_core = [False] * N
    cores = []
    random.seed(42)
    
    # 最初の1つ: 最も密度が高い（疎度が低い）原子を選ぶ
    # ランダム性を持たせるため、上位10%からランダムに選ぶ
    sorted_indices_by_density = sorted(range(N), key=lambda i: local_sparsity[i])
    first_idx = random.choice(sorted_indices_by_density[:max(1, N//10)])
    
    is_core[first_idx] = True
    cores.append(all_components[first_idx])
    
    while len(cores) < M:
        # 既存Coreからの距離を計算
        dist_to_cores = []
        
        for i in range(N):
            if is_core[i]: continue
            
            min_d_to_cores = float('inf')
            cand_atom = atom_objects[i]
            cx, cy = cand_atom.get_pos_at(0, L)
            
            for core in cores:
                core_rep = atom_objects[core.atom_indices[0]]
                rx, ry = core_rep.get_pos_at(0, L)
                d2 = calc_torus_dist_sq(cx, cy, rx, ry, L)
                if d2 < min_d_to_cores:
                    min_d_to_cores = d2
            dist_to_cores.append((min_d_to_cores, i))
            
        # 候補の絞り込み: Coreから遠い順にソートして、上位候補を抽出
        # 分散を担保するため、距離上位 40% を候補とする
        dist_to_cores.sort(key=lambda x: x[0], reverse=True)
        
        num_candidates = max(1, len(dist_to_cores) * 4 // 10)
        top_candidates = dist_to_cores[:num_candidates]
        
        # 上位候補の中で、最も密度が高い（疎度が低い）ものを選ぶ
        best_idx = -1
        min_sparsity = float('inf')
        
        for _, idx in top_candidates:
            if local_sparsity[idx] < min_sparsity:
                min_sparsity = local_sparsity[idx]
                best_idx = idx
                
        is_core[best_idx] = True
        cores.append(all_components[best_idx])
    # # --- Core選定 ---
    # random.seed(42)
    # is_core = [False] * N
    # cores = []
    
    # # 最初の1つ
    # first_idx = random.randint(0, N-1)
    # is_core[first_idx] = True
    # cores.append(all_components[first_idx])
    
    # while len(cores) < M:
    #     best_dist = -1
    #     best_idx = -1
        
    #     # サンプリングで候補を選ぶ
    #     for i in range(N):
    #         if is_core[i]: continue
            
    #         min_d_to_cores = float('inf')
    #         cand_atom = atom_objects[i]
    #         cx, cy = cand_atom.get_pos_at(0, L)
            
    #         for core in cores:
    #             # Coreの代表として最初の原子を使う
    #             core_rep = atom_objects[core.atom_indices[0]]
    #             rx, ry = core_rep.get_pos_at(0, L)
    #             d2 = calc_torus_dist_sq(cx, cy, rx, ry, L)
    #             if d2 < min_d_to_cores:
    #                 min_d_to_cores = d2
            
    #         if min_d_to_cores > best_dist:
    #             best_dist = min_d_to_cores
    #             best_idx = i
                
    #     is_core[best_idx] = True
    #     cores.append(all_components[best_idx])

    # 残りはFreeリストへ
    frees = [all_components[i] for i in range(N) if not is_core[i]]

    operations = []
    start_time = time.time()

    # --- フェーズ時間割の計算 (指数増加) ---
    # 後半の比重を重くする。指数的に増加させる。
    # 1.1^0 = 1, ..., 1.1^28 ≈ 14.4
    # これにより、終盤のフェーズは序盤の約14倍の時間(ターン数)を持つことになる。
    weights = [1.1 ** i for i in range(NUM_GROWTH_PHASES)]
    total_weight = sum(weights)
    
    # 焼きなまし時間(Time Budget)も同様に配分する
    available_time_for_sa = TOTAL_TIME_LIMIT - 0.1
    phase_time_budgets = [available_time_for_sa * (w / total_weight) for w in weights]
    
    phase_end_times = []
    current_end = 0.0
    for w in weights:
        duration = T * (w / total_weight)
        current_end += duration
        phase_end_times.append(current_end)
    
    # 最終ターンは確実にT
    phase_end_times[-1] = T

    # --- 成長フェーズループ (29回) ---
    for phase in range(NUM_GROWTH_PHASES):
        phase_start_time = time.time()
        current_time_budget = phase_time_budgets[phase]
        
        # このフェーズの終了時刻目安
        phase_end_t = phase_end_times[phase]
        # 少し余裕を持たせる（前のフェーズで遅れた場合など）
        search_limit_t = min(T, phase_end_t + 50) 
        
        num_cores = len(cores)
        num_frees = len(frees)
        
        # --- 初期解生成 (Greedy) ---
        used_free_mask = [False] * num_frees
        assignment = [-1] * num_cores # core_idx -> free_idx
        
        for i in range(num_cores):
            core = cores[i]
            best_f_idx = -1
            min_score = float('inf')
            
            # サンプリング探索
            search_indices = random.sample(range(num_frees), min(num_frees, 30))
            
            # Core内の全原子を取得しておく
            core_atoms = [atom_objects[aid] for aid in core.atom_indices]
            
            for f_idx in search_indices:
                if used_free_mask[f_idx]: continue
                free = frees[f_idx]
                free_atom = atom_objects[free.atom_indices[0]] # Freeはサイズ1と仮定
                
                # 時刻概算 (Coreの最新更新時刻)
                # 少なくともCoreの時間は過ぎている必要がある
                base_t = core_atoms[0].t_update
                
                # Core内の各原子との距離の最小値を簡易計算
                # 時間がないので、t=base_t時点での距離で判定
                min_d2_local = float('inf')
                fx, fy = free_atom.get_pos_at(base_t, L)
                
                for ca in core_atoms:
                    cx, cy = ca.get_pos_at(base_t, L)
                    d2 = calc_torus_dist_sq(cx, cy, fx, fy, L)
                    if d2 < min_d2_local:
                        min_d2_local = d2
                
                if min_d2_local < min_score:
                    min_score = min_d2_local
                    best_f_idx = f_idx
            
            if best_f_idx == -1:
                for k in range(num_frees):
                    if not used_free_mask[k]:
                        best_f_idx = k
                        break
            
            assignment[i] = best_f_idx
            used_free_mask[best_f_idx] = True

        # --- 評価関数 ---
        # (core_idx, free_idx) -> (score, meet_t, best_pair_atom_id)
        # スコアには距離と時刻が含まれる
        eval_cache = {}

        def get_eval(c_idx, f_idx):
            key = (c_idx, f_idx)
            if key in eval_cache: return eval_cache[key]
            
            core = cores[c_idx]
            free = frees[f_idx]
            free_atom = atom_objects[free.atom_indices[0]]
            
            core_atoms = [atom_objects[aid] for aid in core.atom_indices]
            
            # 探索開始時刻
            start_search_t = max(core_atoms[0].t_update, free_atom.t_update)
            
            if start_search_t >= search_limit_t:
                # 制限時間を超えてしまう場合は非常に悪いスコア
                return float('inf'), T, -1
            
            # Core内の全原子に対して、Free原子との最接近を計算し、ベストを選ぶ
            best_min_d2 = float('inf')
            best_dt = 0
            best_atom_id = -1
            
            for ca in core_atoms:
                # 相対運動
                dvx = ca.vx - free_atom.vx
                dvy = ca.vy - free_atom.vy
                px, py = ca.get_pos_at(start_search_t, L)
                qx, qy = free_atom.get_pos_at(start_search_t, L)
                
                # 探索範囲は phase_end_t まで (または T まで)
                duration = max(0, search_limit_t - start_search_t)
                
                min_d2, dt = get_trajectory_min_dist(px, py, dvx, dvy, qx, qy, 0, duration, L)
                
                if min_d2 < best_min_d2:
                    best_min_d2 = min_d2
                    best_dt = dt
                    best_atom_id = ca.id
            
            meet_t = start_search_t + best_dt
            
            # スコア: 距離 + 時間ペナルティ
            score = best_min_d2 + TIME_PENALTY * meet_t
            
            eval_cache[key] = (score, meet_t, best_atom_id)
            return score, meet_t, best_atom_id

        # 現在のスコア合計
        current_score = 0
        for i in range(num_cores):
            sc, _, _ = get_eval(i, assignment[i])
            current_score += sc
            
        best_score = current_score
        best_assignment = list(assignment)
        
        # --- 焼きなまし (SA) ---
        sa_iter = 0
        while True:
            sa_iter += 1
            if (sa_iter & 31) == 0:
                if time.time() - phase_start_time > current_time_budget:
                    break
            
            type = random.randint(0, 1)
            
            if type == 0: # Swap
                c1 = random.randint(0, num_cores - 1)
                c2 = random.randint(0, num_cores - 1)
                if c1 == c2: continue
                
                f1 = assignment[c1]
                f2 = assignment[c2]
                
                sc1_old, _, _ = get_eval(c1, f1)
                sc2_old, _, _ = get_eval(c2, f2)
                sc1_new, _, _ = get_eval(c1, f2)
                sc2_new, _, _ = get_eval(c2, f1)
                
                delta = (sc1_new + sc2_new) - (sc1_old + sc2_old)
                
                if delta < 0:
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
                
                sc_old, _, _ = get_eval(c1, f_old)
                sc_new, _, _ = get_eval(c1, f_new)
                
                delta = sc_new - sc_old
                
                if delta < 0:
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
            
            _, meet_t, best_atom_id = get_eval(c_idx, f_idx)
            
            # クランプ
            op_t = min(int(meet_t), T - 1)
            # 原子ごとの時刻と整合性を取る
            min_valid_t = 0
            for aid in core.atom_indices:
                min_valid_t = max(min_valid_t, atom_objects[aid].t_update)
            for aid in free.atom_indices:
                min_valid_t = max(min_valid_t, atom_objects[aid].t_update)
            
            op_t = max(op_t, int(min_valid_t))
            
            # 結合対象の原子ペア
            rep1 = best_atom_id
            if rep1 == -1: rep1 = core.atom_indices[0] # フォールバック
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