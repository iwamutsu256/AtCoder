import sys
import math
import random

# --- クラス定義 ---

class Component:
    """
    連結成分（分子）を表すクラス。
    """
    def __init__(self, c_id, atom_indices, x, y, vx, vy):
        self.id = c_id
        self.atom_indices = atom_indices
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.target_group_id = -1
        self.active = True # 結合されて消滅したかどうか

    def size(self):
        return len(self.atom_indices)

# --- 距離・幾何計算関数 ---

def calc_torus_dist_sq(x1, y1, x2, y2, L):
    """
    トーラス環境下での2点間の距離の二乗を計算する。
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dist_x = min(dx, L - dx)
    dist_y = min(dy, L - dy)
    return dist_x**2 + dist_y**2

def get_trajectory_info(sx, sy, vx, vy, tx, ty, T, L):
    """
    点 (tx, ty) と、原子の軌跡（始点sx,sy, 速度vx,vy）との関係を計算する。
    
    Returns:
        min_d2: 最小距離の二乗
        best_t: 最も近づく時刻 (float)
        best_x, best_y: その時の原子の位置
    """
    min_d2 = float('inf')
    best_t = 0
    best_x = sx
    best_y = sy
    
    A = vx**2 + vy**2
    
    # 動かない場合
    if A == 0:
        d2 = calc_torus_dist_sq(sx, sy, tx, ty, L)
        return d2, 0, sx, sy

    # トーラス考慮（ターゲットを周囲に展開）
    offsets = [-L, 0, L]
    
    for dx_offset in offsets:
        for dy_offset in offsets:
            target_x = tx + dx_offset
            target_y = ty + dy_offset
            
            dx = sx - target_x
            dy = sy - target_y
            
            B = 2 * (vx * dx + vy * dy)
            C = dx**2 + dy**2
            
            # 極値 t = -B / (2A)
            t_extremum = -B / (2 * A)
            
            # 候補時刻: 0, T, 極値
            candidates = [0, T]
            if 0 < t_extremum < T:
                candidates.append(t_extremum)
            
            for t in candidates:
                dist_sq = A * (t**2) + B * t + C
                
                if dist_sq < min_d2:
                    min_d2 = dist_sq
                    best_t = t
                    # その時の位置（正規化前）
                    raw_x = sx + vx * t
                    raw_y = sy + vy * t
                    # 正規化
                    best_x = raw_x % L
                    best_y = raw_y % L
                    
    return min_d2, best_t, best_x, best_y

# --- メインソルバー ---

def solve():
    # 入力高速化
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

    # --- Step 1: 線分クラスタリング (Trajectory K-means) ---
    # 意図: 原子の軌跡(線分)と、重心点(Point)との距離でクラスタリング
    
    random.seed(42)
    # 初期重心: ランダムな原子のランダムな時刻の位置を採用
    centroids = []
    for _ in range(M):
        t_rnd = random.randint(0, T)
        idx_rnd = random.randint(0, N-1)
        cx = (atoms[idx_rnd]['x'] + atoms[idx_rnd]['vx'] * t_rnd) % L
        cy = (atoms[idx_rnd]['y'] + atoms[idx_rnd]['vy'] * t_rnd) % L
        centroids.append((cx, cy))

    # K-means ループ
    atom_info_cache = [None] * N # (gid, best_t, best_x, best_y)
    
    for _ in range(10): # 収束ループ
        # 1. 割り当てフェーズ (距離計算)
        candidates = []
        for i in range(N):
            atom = atoms[i]
            sx, sy, vx, vy = atom['x'], atom['y'], atom['vx'], atom['vy']
            
            for cid in range(M):
                cx, cy = centroids[cid]
                d2, bt, bx, by = get_trajectory_info(sx, sy, vx, vy, cx, cy, T, L)
                candidates.append({
                    'dist': d2,
                    'atom_id': i,
                    'cid': cid,
                    'best_t': bt,
                    'best_x': bx,
                    'best_y': by
                })
        
        # 距離順にソートして定員Kまで割り当て (Greedy Assignment)
        candidates.sort(key=lambda x: x['dist'])
        
        cluster_members = [[] for _ in range(M)] # 各クラスターのメンバー情報
        cluster_counts = [0] * M
        assigned = [False] * N
        
        for cand in candidates:
            aid = cand['atom_id']
            cid = cand['cid']
            
            if assigned[aid]: continue
            if cluster_counts[cid] >= K: continue
            
            assigned[aid] = True
            cluster_counts[cid] += 1
            
            # メンバー追加 (重心更新用に、最接近座標を記録)
            cluster_members[cid].append(cand)
            
            # 最終的な所属情報をキャッシュ
            atom_info_cache[aid] = cand

        # 2. 重心更新フェーズ
        new_centroids = []
        for cid in range(M):
            members = cluster_members[cid]
            if not members:
                new_centroids.append((random.uniform(0, L), random.uniform(0, L)))
                continue
            
            # メンバーが最接近した座標の平均を新しい重心とする
            # トーラス環境での平均計算
            base_x = members[0]['best_x']
            base_y = members[0]['best_y']
            sum_x, sum_y = 0, 0
            
            for m in members:
                tx, ty = m['best_x'], m['best_y']
                dx = tx - base_x
                dy = ty - base_y
                if dx > L/2: dx -= L
                elif dx < -L/2: dx += L
                if dy > L/2: dy -= L
                elif dy < -L/2: dy += L
                sum_x += (base_x + dx)
                sum_y += (base_y + dy)
                
            avg_x = (sum_x / len(members)) % L
            avg_y = (sum_y / len(members)) % L
            new_centroids.append((avg_x, avg_y))
            
        centroids = new_centroids

    # --- Step 2: 結合スケジューリング ---
    # グループ内で「重心に到着する時刻」順にソートし、ペアを作って平均時刻に予約する
    
    scheduled_merges = {} # time -> list of (id1, id2)
    
    # 最終的なグループ分け結果を取得
    final_groups = [[] for _ in range(M)]
    for i in range(N):
        info = atom_info_cache[i]
        final_groups[info['cid']].append(info)
        
    for cid in range(M):
        members = final_groups[cid]
        # 到着時刻順にソート
        members.sort(key=lambda x: x['best_t'])
        
        # 前から2つずつペアにする
        for i in range(0, len(members) - 1, 2):
            m1 = members[i]
            m2 = members[i+1]
            
            # 結合予定時刻 (平均)
            plan_t = int((m1['best_t'] + m2['best_t']) / 2)
            plan_t = max(0, min(T-1, plan_t)) # 範囲内に収める
            
            if plan_t not in scheduled_merges:
                scheduled_merges[plan_t] = []
            
            scheduled_merges[plan_t].append((m1['atom_id'], m2['atom_id']))

    # --- Step 3: シミュレーション実行 ---
    
    # コンポーネント初期化
    components = {} # activeなコンポーネントを map で管理 {id: Component}
    # atom_id -> component_id の逆引きマップ
    atom_to_component = {}
    
    for atom in atoms:
        aid = atom['id']
        c = Component(aid, [aid], atom['x'], atom['y'], atom['vx'], atom['vy'])
        c.target_group_id = atom_info_cache[aid]['cid']
        components[aid] = c
        atom_to_component[aid] = aid

    operations = []

    for t in range(T):
        merged_ids_this_turn = set()
        
        # 1. 予約された結合の実行
        if t in scheduled_merges:
            for aid1, aid2 in scheduled_merges[t]:
                # 現在のコンポーネントIDを取得
                cid1 = atom_to_component[aid1]
                cid2 = atom_to_component[aid2]
                
                # 既に結合済みなどで同じになっていたらスキップ
                if cid1 == cid2: continue
                if cid1 not in components or cid2 not in components: continue
                
                c1 = components[cid1]
                c2 = components[cid2]
                
                # 結合実行
                op_str = f"{t} {c1.atom_indices[0]} {c2.atom_indices[0]}"
                operations.append(op_str)
                
                # 新成分作成
                new_size = c1.size() + c2.size()
                new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
                new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
                
                new_c = Component(c1.id, c1.atom_indices + c2.atom_indices, c1.x, c1.y, new_vx, new_vy)
                new_c.target_group_id = c1.target_group_id
                
                # 管理情報の更新
                del components[cid1]
                del components[cid2]
                components[new_c.id] = new_c
                
                for aid in new_c.atom_indices:
                    atom_to_component[aid] = new_c.id
                    
                merged_ids_this_turn.add(new_c.id)

        # 2. 残党処理 (Greedy Fallback)
        # 予約結合が終わった後、サイズ30を目指して、同じグループの近くにいるものを結合する
        # ※毎回やると重いので、適度な間隔で、あるいは予約がないときにやる
        
        # グループごとに分類
        groups = {}
        for c in components.values():
            if c.id in merged_ids_this_turn: continue
            gid = c.target_group_id
            if gid not in groups: groups[gid] = []
            groups[gid].append(c)
            
        # 閾値（後半ほど緩く）
        threshold = (2000 + (t/T)*50000)**2
        if t > T - 100: threshold = float('inf')
        
        for gid, members in groups.items():
            if len(members) < 2: continue
            
            # 単純な総当たり（グループ内は人数少ないのでOK）
            # 貪欲に「一番近いペア」をくっつけていく
            members.sort(key=lambda x: x.size()) # サイズ小さい順に見るなど工夫も可
            
            skip_indices = set()
            pairs = []
            
            for i in range(len(members)):
                if i in skip_indices: continue
                best_j = -1
                min_d = threshold
                
                c1 = members[i]
                
                for j in range(i+1, len(members)):
                    if j in skip_indices: continue
                    c2 = members[j]
                    
                    if c1.size() + c2.size() > K: continue
                    
                    d2 = calc_torus_dist_sq(c1.x, c1.y, c2.x, c2.y, L)
                    if d2 < min_d:
                        min_d = d2
                        best_j = j
                
                if best_j != -1:
                    skip_indices.add(i)
                    skip_indices.add(best_j)
                    pairs.append((c1, members[best_j]))
            
            # ペア結合実行
            for c1, c2 in pairs:
                op_str = f"{t} {c1.atom_indices[0]} {c2.atom_indices[0]}"
                operations.append(op_str)
                
                new_size = c1.size() + c2.size()
                new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
                new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
                
                new_c = Component(c1.id, c1.atom_indices + c2.atom_indices, c1.x, c1.y, new_vx, new_vy)
                new_c.target_group_id = gid
                
                del components[c1.id]
                del components[c2.id]
                components[new_c.id] = new_c
                for aid in new_c.atom_indices:
                    atom_to_component[aid] = new_c.id

        # 3. 移動
        for c in components.values():
            c.x = (c.x + c.vx) % L
            c.y = (c.y + c.vy) % L

    for op in operations:
        print(op)

if __name__ == "__main__":
    solve()