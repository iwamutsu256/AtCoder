import sys
import math
import random
import time

# --- 定数・設定 ---
TIME_LIMIT = 1.8  # 制限時間(秒)

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

# --- シミュレーション関数 ---

def run_simulation(N, T, M, K, L, atoms, assignments):
    """
    指定されたグループ割り当て(assignments)に基づいてシミュレーションを行い、
    総コストと操作列を返す。
    
    Args:
        assignments: 長さNのリスト。atoms[i]の所属グループID。
    
    Returns:
        total_cost: 結合コストの合計
        operations: 操作ログのリスト ["t i j", ...]
    """
    
    # --- データ構造の初期化 ---
    # 高速化のため、クラスを使わず辞書とリストで管理
    
    active_components = {}
    groups = [set() for _ in range(M)]
    
    # 初期化
    for i in range(N):
        atom = atoms[i]
        gid = assignments[i]
        
        # コンポーネントデータ
        # x, y, vx, vy, size, representative_atom_id
        comp = [
            atom['x'], atom['y'], 
            atom['vx'], atom['vy'], 
            1, i
        ]
        
        active_components[i] = comp
        groups[gid].add(i)

    operations = []
    total_cost = 0
    
    # --- シミュレーションループ ---
    for t in range(T):
        
        processed_ids = set() # このターンで結合に参加したID
        
        # 各グループ内で結合ペアを探す
        for gid in range(M):
            member_ids = list(groups[gid])
            if len(member_ids) < 2: continue
            
            # 距離計算用リスト作成
            current_mems = []
            for cid in member_ids:
                if cid in processed_ids: continue
                current_mems.append((cid, active_components[cid]))
            
            # ペア探索
            # 貪欲に「一番近いペア」を見つけては結合、を繰り返す
            while len(current_mems) >= 2:
                best_pair = None
                min_d2 = float('inf')
                best_idx_pair = (-1, -1)
                
                n = len(current_mems)
                
                # 総当たり
                for i in range(n):
                    cid1, c1 = current_mems[i]
                    for j in range(i + 1, n):
                        cid2, c2 = current_mems[j]
                        
                        # サイズ制限チェック
                        if c1[4] + c2[4] > K: continue
                        
                        d2 = calc_torus_dist_sq(c1[0], c1[1], c2[0], c2[1], L)
                        
                        if d2 < min_d2:
                            min_d2 = d2
                            best_pair = (cid1, cid2)
                            best_idx_pair = (i, j)
                
                if best_pair:
                    cid1, cid2 = best_pair
                    idx1, idx2 = best_idx_pair
                    c1 = active_components[cid1]
                    c2 = active_components[cid2]
                    
                    total_cost += round(min_d2)
                    
                    # 操作記録
                    rep1 = c1[5]
                    rep2 = c2[5]
                    operations.append(f"{t} {rep1} {rep2}")
                    
                    # 新コンポーネント作成
                    new_size = c1[4] + c2[4]
                    new_vx = (c1[4] * c1[2] + c2[4] * c2[2]) / new_size
                    new_vy = (c1[4] * c1[3] + c2[4] * c2[3]) / new_size
                    new_comp = [c1[0], c1[1], new_vx, new_vy, new_size, rep1]
                    
                    # データ更新
                    current_mems.pop(idx2)
                    current_mems.pop(idx1)
                    
                    processed_ids.add(cid1)
                    processed_ids.add(cid2)
                    
                    del active_components[cid2]
                    active_components[cid1] = new_comp
                    groups[gid].remove(cid2)
                    
                else:
                    break
                    
        # --- 移動フェーズ ---
        for cid, comp in active_components.items():
            comp[0] = (comp[0] + comp[2]) % L
            comp[1] = (comp[1] + comp[3]) % L
            
    return total_cost, operations

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
            'x': x, 'y': y, 'vx': vx, 'vy': vy
        })

    # --- タイマー開始 ---
    start_time = time.time()

    # --- 初期解生成: K-means ---
    random.seed(42)
    initial_indices = random.sample(range(N), M)
    centroids = [(atoms[i]['x'], atoms[i]['y']) for i in initial_indices]

    for _ in range(10): # K-means loop
        # 所属決定
        temp_clusters = [[] for _ in range(M)]
        for i in range(N):
            ax, ay = atoms[i]['x'], atoms[i]['y']
            best_d2 = float('inf')
            best_cid = -1
            for cid in range(M):
                cx, cy = centroids[cid]
                d2 = calc_torus_dist_sq(ax, ay, cx, cy, L)
                if d2 < best_d2:
                    best_d2 = d2
                    best_cid = cid
            temp_clusters[best_cid].append(i)
        
        # 重心更新
        new_centroids = []
        for cid in range(M):
            mems = temp_clusters[cid]
            if not mems:
                new_centroids.append((random.uniform(0,L), random.uniform(0,L)))
                continue
            
            base_x, base_y = atoms[mems[0]]['x'], atoms[mems[0]]['y']
            sum_x, sum_y = 0, 0
            for idx in mems:
                tx, ty = atoms[idx]['x'], atoms[idx]['y']
                dx = tx - base_x
                dy = ty - base_y
                if dx > L/2: dx -= L
                elif dx < -L/2: dx += L
                if dy > L/2: dy -= L
                elif dy < -L/2: dy += L
                sum_x += base_x + dx
                sum_y += base_y + dy
            new_centroids.append(((sum_x/len(mems))%L, (sum_y/len(mems))%L))
        centroids = new_centroids
        
    # K-meansの結果に基づき、サイズ制約を満たす初期割り当てを作成
    candidates = []
    for i in range(N):
        ax, ay = atoms[i]['x'], atoms[i]['y']
        for cid in range(M):
            cx, cy = centroids[cid]
            d2 = calc_torus_dist_sq(ax, ay, cx, cy, L)
            candidates.append((d2, i, cid))
    candidates.sort(key=lambda x: x[0])
    
    current_assignments = [-1] * N
    cluster_counts = [0] * M
    assigned_count = 0
    for _, idx, cid in candidates:
        if assigned_count == N: break
        if current_assignments[idx] != -1: continue
        if cluster_counts[cid] >= K: continue
        current_assignments[idx] = cid
        cluster_counts[cid] += 1
        assigned_count += 1
        
    # --- 山登り法 (Hill Climbing) ---
    
    # コスト行列の事前計算
    cost_matrix = [[0] * M for _ in range(N)]
    for i in range(N):
        ax, ay = atoms[i]['x'], atoms[i]['y']
        for cid in range(M):
            cx, cy = centroids[cid]
            cost_matrix[i][cid] = calc_torus_dist_sq(ax, ay, cx, cy, L)

    # 現在の軽量コスト計算と、各原子のコスト保持
    current_score = 0
    current_atom_costs = [0.0] * N  # 各原子の現在の「重心との距離」
    
    for i in range(N):
        c = cost_matrix[i][current_assignments[i]]
        current_atom_costs[i] = c
        current_score += c
    
    best_score = current_score
    best_assignments = list(current_assignments)
    
    loop_count = 0
    
    while time.time() - start_time < TIME_LIMIT:
        loop_count += 1
        
        # --- 近傍操作: 悪い原子を優先的にSwap ---
        
        # idx1の選択: 「トーナメント選択」でコストが高い（重心から遠い）原子を選ぶ
        # ランダムに数個ピックアップし、その中で一番悪いやつをSwap候補にする
        
        tournament_size = 5
        best_bad_val = -1
        idx1 = -1
        
        # ランダムサンプリング（重複なし）
        for cand_idx in random.sample(range(N), tournament_size):
            val = current_atom_costs[cand_idx]
            if val > best_bad_val:
                best_bad_val = val
                idx1 = cand_idx
                
        # idx2の選択: こちらはランダムに選ぶ（受け入れ先を探す）
        idx2 = random.randint(0, N-1)
        
        gid1 = current_assignments[idx1]
        gid2 = current_assignments[idx2]
        
        if gid1 == gid2:
            continue
            
        # 差分計算 (軽量)
        cost1_old = cost_matrix[idx1][gid1]
        cost2_old = cost_matrix[idx2][gid2]
        
        cost1_new = cost_matrix[idx1][gid2]
        cost2_new = cost_matrix[idx2][gid1]
        
        delta = (cost1_new + cost2_new) - (cost1_old + cost2_old)
        
        if delta < 0:
            # 改善: 採用
            current_assignments[idx1] = gid2
            current_assignments[idx2] = gid1
            
            # コスト情報の更新（次のトーナメント選択のために重要）
            current_atom_costs[idx1] = cost1_new
            current_atom_costs[idx2] = cost2_new
            
            current_score += delta
            
            if current_score < best_score:
                best_score = current_score
                best_assignments = list(current_assignments)
        
    # --- 最終出力 ---
    sys.stderr.write(f"Loops: {loop_count}, Best Proxy Score: {best_score}\n")
    
    _, final_ops = run_simulation(N, T, M, K, L, atoms, best_assignments)
    for op in final_ops:
        print(op)

if __name__ == "__main__":
    solve()