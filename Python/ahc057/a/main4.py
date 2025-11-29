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

    def size(self):
        return len(self.atom_indices)

# --- 距離計算関数 ---

def calc_torus_dist_sq(x1, y1, x2, y2, L):
    """
    トーラス環境下での2点間の距離の二乗を計算する。
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dist_x = min(dx, L - dx)
    dist_y = min(dy, L - dy)
    return dist_x**2 + dist_y**2

def predict_collision(c1, c2, L, look_ahead_steps):
    """
    2つの成分 c1, c2 について、現在から look_ahead_steps ターンの間で
    最も距離が小さくなるタイミングと、その時の距離を計算する。

    Args:
        c1, c2: Component
        L: 空間サイズ
        look_ahead_steps: 何ターン先まで予測するか

    Returns:
        (best_wait_time, min_dist_sq): 
            best_wait_time: 何ターン後がベストか (0なら「今」)
            min_dist_sq: その時の距離の二乗
    """
    best_t = 0
    min_d2 = float('inf')

    # シミュレーション用の一時座標
    x1, y1 = c1.x, c1.y
    x2, y2 = c2.x, c2.y
    
    # 相対速度
    # c1を止めてc2が動くと考えても距離計算は同じだが、
    # トーラスがあるので愚直に両方動かして計算するのが安全かつ実装が楽
    vx1, vy1 = c1.vx, c1.vy
    vx2, vy2 = c2.vx, c2.vy

    for t in range(look_ahead_steps + 1):
        # 現在時刻 t における距離計算
        d2 = calc_torus_dist_sq(x1, y1, x2, y2, L)
        
        if d2 < min_d2:
            min_d2 = d2
            best_t = t
            
            # 距離0ならこれ以上調べる必要なし（即リターンでも良いが、念の為ループ継続させない）
            if d2 == 0:
                break
        
        # 次のステップへ位置更新
        x1 = (x1 + vx1) % L
        y1 = (y1 + vy1) % L
        x2 = (x2 + vx2) % L
        y2 = (y2 + vy2) % L

    return best_t, min_d2

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

    # コンポーネント初期化
    components = []
    for atom in atoms:
        c = Component(atom['id'], [atom['id']], atom['x'], atom['y'], atom['vx'], atom['vy'])
        components.append(c)

    # --- Step 1: K-meansによるグループ分け (前回同様) ---
    # 2次元的に近いものをグループ化し、target_group_idを割り当てる
    
    random.seed(42)
    initial_indices = random.sample(range(N), M)
    centroids = [(atoms[i]['x'], atoms[i]['y']) for i in initial_indices]

    # K-means ループ
    for _ in range(15): # 少し回数を増やす
        temp_clusters = [[] for _ in range(M)]
        
        for i in range(N):
            ax, ay = atoms[i]['x'], atoms[i]['y']
            best_dist = float('inf')
            best_cid = -1
            for cid in range(M):
                cx, cy = centroids[cid]
                d2 = calc_torus_dist_sq(ax, ay, cx, cy, L)
                if d2 < best_dist:
                    best_dist = d2
                    best_cid = cid
            temp_clusters[best_cid].append(i)
        
        new_centroids = []
        for cid in range(M):
            members = temp_clusters[cid]
            if not members:
                new_centroids.append((random.uniform(0, L), random.uniform(0, L)))
                continue
            
            base_x, base_y = atoms[members[0]]['x'], atoms[members[0]]['y']
            sum_x, sum_y = 0, 0
            for idx in members:
                tx, ty = atoms[idx]['x'], atoms[idx]['y']
                dx = tx - base_x
                dy = ty - base_y
                if dx > L/2: dx -= L
                elif dx < -L/2: dx += L
                if dy > L/2: dy -= L
                elif dy < -L/2: dy += L
                sum_x += (base_x + dx)
                sum_y += (base_y + dy)
            new_centroids.append(((sum_x/len(members))%L, (sum_y/len(members))%L))
        centroids = new_centroids

    # サイズ制約付き割り当て
    candidates = []
    for i in range(N):
        ax, ay = atoms[i]['x'], atoms[i]['y']
        for cid in range(M):
            cx, cy = centroids[cid]
            d2 = calc_torus_dist_sq(ax, ay, cx, cy, L)
            candidates.append((d2, i, cid))
    
    candidates.sort(key=lambda x: x[0])
    
    cluster_counts = [0] * M
    assigned_count = 0
    atom_target_group = [-1] * N
    
    for _, atom_idx, cid in candidates:
        if assigned_count == N: break
        if atom_target_group[atom_idx] != -1: continue
        if cluster_counts[cid] >= K: continue
        
        atom_target_group[atom_idx] = cid
        cluster_counts[cid] += 1
        assigned_count += 1
        components[atom_idx].target_group_id = cid

    active_components = components[:]
    operations = []

    # --- Step 2: シミュレーション & 予測付き結合 ---
    
    for t in range(T):
        merged_indices = set()
        next_active_components = []
        
        # グループ化
        groups = {}
        for c in active_components:
            gid = c.target_group_id
            if gid not in groups: groups[gid] = []
            groups[gid].append(c)

        # 結合候補リスト: (cost, component1, component2)
        merge_candidates = []
        
        # 予測期間: 最初は長く、終盤は短くしても良いが、
        # 相対速度が最大200+200=400程度、L=100000なので、
        # すれ違うのに最短でも L/400 = 250ターンかかる。
        # ただ、近くのものを拾いたいので 20〜50ターン程度先読みすれば十分。
        look_ahead = 30 
        
        # 終盤の強制回収モード
        if t > T - 150:
            look_ahead = 0 # 未来を見ずに今すぐ結合するモード

        processed_current_step = set()

        # 各グループ内で候補を探す
        for gid, members in groups.items():
            if len(members) < 2: continue
            
            n_mem = len(members)
            for i in range(n_mem):
                for j in range(i + 1, n_mem):
                    c1 = members[i]
                    c2 = members[j]
                    
                    if c1.size() + c2.size() > K: continue

                    # --- アルゴリズム核心部: 未来予測 ---
                    # 2つの成分が今後 look_ahead ターンの間にどう動くか計算し、
                    # 「今結合すべきか（今が一番近いか）」を判定する。
                    
                    best_wait, min_d2 = predict_collision(c1, c2, L, look_ahead)
                    
                    # 「今が一番近い」(= これ以上待つと離れる) 場合のみ、候補に入れる。
                    # または、距離が極端に近い場合も候補に入れる。
                    if best_wait == 0:
                        merge_candidates.append((min_d2, c1, c2))

        # コストが小さい順に結合を実行（貪欲法）
        merge_candidates.sort(key=lambda x: x[0])
        
        for cost, c1, c2 in merge_candidates:
            # 既にこのターンで他のものと結合してしまったらスキップ
            if c1 in processed_current_step or c2 in processed_current_step:
                continue
            
            # 結合実行
            atom_i = c1.atom_indices[0]
            atom_j = c2.atom_indices[0]
            operations.append(f"{t} {atom_i} {atom_j}")
            
            new_size = c1.size() + c2.size()
            new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
            new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
            
            new_c = Component(atom_i, c1.atom_indices + c2.atom_indices, c1.x, c1.y, new_vx, new_vy)
            new_c.target_group_id = c1.target_group_id # どちらも同じはず
            
            processed_current_step.add(c1)
            processed_current_step.add(c2)
            next_active_components.append(new_c)

        # 結合しなかったものを次へ
        for c in active_components:
            if c not in processed_current_step:
                next_active_components.append(c)
        
        active_components = next_active_components

        # 移動
        for c in active_components:
            c.x = (c.x + c.vx) % L
            c.y = (c.y + c.vy) % L

    for op in operations:
        print(op)

if __name__ == "__main__":
    solve()