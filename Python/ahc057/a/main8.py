import sys
import math
import random
import time

# --- 定数・設定 ---
# 未来予測をする期間の長さ
LOOKAHEAD_STEPS = 200 

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

def get_trajectory_min_dist(sx, sy, vx, vy, tx, ty, limit_t, L):
    """
    始点(sx,sy), 速度(vx,vy) の軌道と、点(tx,ty) との
    limit_t ターン以内の最小距離の二乗とその時の経過時間を返す。
    """
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
            
            candidates = [0, limit_t]
            if 0 < t_extremum < limit_t:
                candidates.append(t_extremum)
            
            for t in candidates:
                dist_sq = A * (t**2) + B * t + C
                if dist_sq < min_d2:
                    min_d2 = dist_sq
                    best_dt = t
                    
    return min_d2, best_dt

# --- クラス定義 ---

class Component:
    def __init__(self, c_id, atom_indices, vx, vy, gid):
        self.id = c_id
        self.atom_indices = atom_indices # list of atom IDs
        self.vx = float(vx)
        self.vy = float(vy)
        self.target_group_id = gid
    
    def size(self):
        return len(self.atom_indices)

# --- メインソルバー ---

def solve():
    # 入力処理
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

    # ---------------------------------------------------------
    # Step 1: K-means法による初期グループ割り当て
    # ---------------------------------------------------------
    random.seed(42)
    centroids = []
    for _ in range(M):
        idx = random.randint(0, N-1)
        t_rnd = random.randint(0, T)
        cx = (atoms[idx]['x'] + atoms[idx]['vx'] * t_rnd) % L
        cy = (atoms[idx]['y'] + atoms[idx]['vy'] * t_rnd) % L
        centroids.append((cx, cy))

    atom_assignments = [-1] * N
    
    for _ in range(12): 
        candidates = []
        for i in range(N):
            atom = atoms[i]
            # 軌道と重心の距離でクラスタリング
            best_dist = float('inf')
            best_cid = -1
            best_pos = (atom['x'], atom['y'])
            
            for cid in range(M):
                cx, cy = centroids[cid]
                d2, dt = get_trajectory_min_dist(atom['x'], atom['y'], atom['vx'], atom['vy'], cx, cy, T, L)
                if d2 < best_dist:
                    best_dist = d2
                    best_cid = cid
                    px = (atom['x'] + atom['vx'] * dt) % L
                    py = (atom['y'] + atom['vy'] * dt) % L
                    best_pos = (px, py)
            
            candidates.append({
                'dist': best_dist, 'aid': i, 'cid': best_cid, 'pos': best_pos
            })
            
        candidates.sort(key=lambda x: x['dist'])
        cluster_counts = [0] * M
        atom_assignments = [-1] * N
        assigned_count = 0
        cluster_positions = [[] for _ in range(M)]
        
        for cand in candidates:
            if assigned_count == N: break
            aid = cand['aid']
            cid = cand['cid']
            if atom_assignments[aid] != -1: continue
            if cluster_counts[cid] >= K: continue
            
            atom_assignments[aid] = cid
            cluster_counts[cid] += 1
            assigned_count += 1
            cluster_positions[cid].append(cand['pos'])
            
        new_centroids = []
        for cid in range(M):
            positions = cluster_positions[cid]
            if not positions:
                new_centroids.append((random.uniform(0, L), random.uniform(0, L)))
                continue
            
            base_x, base_y = positions[0]
            sum_x, sum_y = 0, 0
            for px, py in positions:
                dx = px - base_x
                dy = py - base_y
                if dx > L/2: dx -= L
                elif dx < -L/2: dx += L
                if dy > L/2: dy -= L
                elif dy < -L/2: dy += L
                sum_x += base_x + dx
                sum_y += base_y + dy
            new_centroids.append(((sum_x/len(positions))%L, (sum_y/len(positions))%L))
        centroids = new_centroids

    # ---------------------------------------------------------
    # Step 2: 動的予測貪欲シミュレーション (Atom-Level Distance)
    # ---------------------------------------------------------
    
    active_components = []
    # コンポーネントはもはや代表位置を持たず、atoms配列の座標を参照する
    for i in range(N):
        atom = atoms[i]
        # x,yは個別のatoms配列で管理するためComponentには持たせない
        c = Component(i, [i], atom['vx'], atom['vy'], atom_assignments[i])
        active_components.append(c)

    operations = []

    for t in range(T):
        
        groups = {}
        for c in active_components:
            gid = c.target_group_id
            if gid not in groups: groups[gid] = []
            groups[gid].append(c)
            
        processed_ids = set()
        next_active_components = []
        
        # 強制モード: 残り200ターン
        force_mode = (t > T - 200)

        if force_mode:
            # --- 強制結合: 残っているものを単純に結合 ---
            # グループ内総量はKなので、無条件に結合して1つにまとめる
            for gid, members in groups.items():
                valid_members = [m for m in members if m.id not in processed_ids]
                
                # 単純にリストの先頭から順に結合していく
                while len(valid_members) >= 2:
                    c1 = valid_members.pop(0)
                    # 一番近い相手を探す（少しでもスコアを良くするため）
                    best_partner_idx = -1
                    min_pair_dist = float('inf')
                    best_pair_atoms = (-1, -1)
                    
                    for i, c2 in enumerate(valid_members):
                        # 原子レベルでの距離計算
                        # c1の全原子 vs c2の全原子
                        for a1 in c1.atom_indices:
                            for a2 in c2.atom_indices:
                                d2 = calc_torus_dist_sq(atoms[a1]['x'], atoms[a1]['y'], 
                                                        atoms[a2]['x'], atoms[a2]['y'], L)
                                if d2 < min_pair_dist:
                                    min_pair_dist = d2
                                    best_partner_idx = i
                                    best_pair_atoms = (a1, a2)
                    
                    if best_partner_idx != -1:
                        c2 = valid_members.pop(best_partner_idx)
                        a1, a2 = best_pair_atoms
                        
                        # 結合実行
                        processed_ids.add(c1.id)
                        processed_ids.add(c2.id)
                        
                        operations.append(f"{t} {a1} {a2}")
                        
                        new_size = c1.size() + c2.size()
                        new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
                        new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
                        
                        new_c = Component(c1.id, c1.atom_indices + c2.atom_indices, new_vx, new_vy, gid)
                        next_active_components.append(new_c)
                        
                        # 新しい成分をvalid_membersに戻して、さらに結合を続ける
                        # (1つにまとまるまで繰り返すため)
                        valid_members.insert(0, new_c)
                    else:
                        # ここには来ないはずだが念のため
                        next_active_components.append(c1)

        else:
            # --- 通常モード: 予測貪欲 ---
            candidates = []
            
            progress = t / T
            threshold_dist = 2000 + progress * 50000 
            threshold_sq = threshold_dist ** 2
            
            for gid, members in groups.items():
                if len(members) < 2: continue
                
                n_mem = len(members)
                # 総当たり
                for i in range(n_mem):
                    for j in range(i + 1, n_mem):
                        c1 = members[i]
                        c2 = members[j]
                        
                        if c1.size() + c2.size() > K: continue

                        # 原子レベルでの現在距離最小ペアを探す
                        min_now_d2 = float('inf')
                        best_atoms = (-1, -1)
                        
                        # 重たい計算になりうるので、成分サイズが大きい場合は
                        # 代表点(重心)で簡易チェックしてから詳細計算するなどの枝刈りが有効だが
                        # K=30, グループ数10, メンバー数少なので恐らく間に合う
                        for a1 in c1.atom_indices:
                            for a2 in c2.atom_indices:
                                d2 = calc_torus_dist_sq(atoms[a1]['x'], atoms[a1]['y'], 
                                                        atoms[a2]['x'], atoms[a2]['y'], L)
                                if d2 < min_now_d2:
                                    min_now_d2 = d2
                                    best_atoms = (a1, a2)
                        
                        # 未来予測 (相対運動)
                        # ここでは簡易的に、現在最も近い原子ペアの相対運動で予測する
                        # (厳密には回転しないので全ペア同じ相対運動をするはず)
                        # -> 成分全体で速度は同じなので、どの原子ペアで見ても相対速度は同じ。
                        # -> 初期の相対位置だけが違う。
                        # -> つまり、全原子ペアの距離推移は平行移動したグラフになる。
                        # -> 「最も近づくタイミング」は全ペアほぼ同じになるはず。
                        
                        a1_id, a2_id = best_atoms
                        a1_obj, a2_obj = atoms[a1_id], atoms[a2_id]
                        
                        future_d2, best_dt = get_trajectory_min_dist(
                            a1_obj['x'], a1_obj['y'], c1.vx, c1.vy, 
                            a2_obj['x'], a2_obj['y'], LOOKAHEAD_STEPS, L
                        )
                        
                        should_merge = False
                        
                        if best_dt <= 1.0:
                            if min_now_d2 < threshold_sq:
                                should_merge = True
                        else:
                            if min_now_d2 < future_d2 * 1.2 and min_now_d2 < threshold_sq:
                                should_merge = True
                            if min_now_d2 < (500**2):
                                should_merge = True
                        
                        if should_merge:
                            candidates.append((min_now_d2, c1, c2, best_atoms))

            candidates.sort(key=lambda x: x[0])
            
            for d2, c1, c2, (a1, a2) in candidates:
                if c1.id in processed_ids or c2.id in processed_ids:
                    continue
                
                processed_ids.add(c1.id)
                processed_ids.add(c2.id)
                
                operations.append(f"{t} {a1} {a2}")
                
                new_size = c1.size() + c2.size()
                new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
                new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
                
                new_c = Component(c1.id, c1.atom_indices + c2.atom_indices, new_vx, new_vy, c1.target_group_id)
                next_active_components.append(new_c)
            
        # 未処理のものを引き継ぎ
        for c in active_components:
            if c.id not in processed_ids:
                next_active_components.append(c)
                
        active_components = next_active_components
        
        # --- 移動フェーズ: 全原子の位置を更新 ---
        # 各原子は所属するコンポーネントの速度で移動する
        
        # componentの速度を参照するためのマップ
        comp_map = {}
        for c in active_components:
            comp_map[c.id] = c
            
        # atomsごとの所属Component IDを追跡する必要があるが
        # active_components内のatom_indicesを見ればわかる
        # しかし毎回検索するのは遅いので、atom_id -> comp (or vx, vy) のマップを作る
        
        atom_vx = [0.0] * N
        atom_vy = [0.0] * N
        
        for c in active_components:
            for aid in c.atom_indices:
                atom_vx[aid] = c.vx
                atom_vy[aid] = c.vy
        
        for i in range(N):
            atoms[i]['x'] = (atoms[i]['x'] + atom_vx[i]) % L
            atoms[i]['y'] = (atoms[i]['y'] + atom_vy[i]) % L

    for op in operations:
        print(op)

if __name__ == "__main__":
    solve()