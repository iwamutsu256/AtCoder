import sys
import math
import random  # K-meansの初期化に使用

# --- クラス定義: Union-Findのような構造で連結成分を管理 ---

class Component:
    """
    連結成分（分子）を表すクラス。
    複数の原子（Atom）が結合して1つのComponentになります。
    """
    def __init__(self, c_id, atom_indices, x, y, vx, vy):
        """
        初期化
        
        Args:
            c_id (int): コンポーネントID（代表元）
            atom_indices (list): この成分に含まれる原子のインデックスリスト
            x, y (float): 重心座標
            vx, vy (int): 速度
        """
        self.id = c_id
        self.atom_indices = atom_indices  # この成分に含まれる原子IDのリスト
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.target_group_id = -1  # 戦略上、どの最終グループに属する予定か

    def size(self):
        """現在の構成原子数を返す"""
        return len(self.atom_indices)

# --- 距離計算関数 ---

def calc_torus_dist_sq(x1, y1, x2, y2, L):
    """
    トーラス環境下での2点間の距離の二乗を計算する。
    
    Args:
        x1, y1: 点1の座標
        x2, y2: 点2の座標
        L: 空間の一辺の長さ
    
    Returns:
        int: 距離の二乗（問題文のコスト定義に従いroundする前の値だが、比較用に使用）
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    
    # トーラスなので、Lをまたぐ逆側の距離と比較して小さい方を取る
    dist_x = min(dx, L - dx)
    dist_y = min(dy, L - dy)
    
    return dist_x**2 + dist_y**2

# --- メインソルバー ---

def solve():
    """
    AHC057のメイン解決関数。
    標準入力からデータを読み込み、貪欲法に基づいて操作を出力する。
    """
    
    # --- 入力の読み込み ---
    # input() は遅い可能性があるため sys.stdin.readline を使用
    input = sys.stdin.readline
    
    # 最初の行: N, T, M, K, L
    try:
        line1 = input().split()
        if not line1: return # 入力が空の場合
        N, T, M, K, L = map(int, line1)
    except ValueError:
        return

    # 各原子の初期情報を読み込む
    atoms = []
    for i in range(N):
        x, y, vx, vy = map(int, input().split())
        atoms.append({
            'id': i,
            'x': x, 'y': y,
            'vx': vx, 'vy': vy
        })

    # --- 初期化プロセス ---
    
    # 現在の全コンポーネントを管理するリスト
    components = []
    for atom in atoms:
        c = Component(atom['id'], [atom['id']], atom['x'], atom['y'], atom['vx'], atom['vy'])
        components.append(c)

    # --- 戦略: 初期グループ分け (Constrained K-means) ---
    # 最終的に作るのはサイズK(30)のグループM(10)個。
    # 2次元的に近い点を集めるため、簡易的なK-means法を用いてグループIDを割り振る。
    
    # 1. 重心（Centroids）の初期化
    # ランダムにM個の原子の位置を初期重心とする
    # 再現性のためシードを固定（コンテストでは外しても良い）
    random.seed(42)
    initial_indices = random.sample(range(N), M)
    centroids = [(atoms[i]['x'], atoms[i]['y']) for i in initial_indices]

    # 2. 重心の更新ループ (数回回して重心位置を安定させる)
    for _ in range(10):
        temp_clusters = [[] for _ in range(M)]
        
        # 全点を一番近い重心に割り当て
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
        
        # 重心の更新
        new_centroids = []
        for cid in range(M):
            members = temp_clusters[cid]
            if not members:
                new_centroids.append((random.uniform(0, L), random.uniform(0, L)))
                continue
            
            # トーラス環境での重心計算
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
            
            avg_x = (sum_x / len(members)) % L
            avg_y = (sum_y / len(members)) % L
            new_centroids.append((avg_x, avg_y))
        
        centroids = new_centroids

    # 3. サイズ制約付き割り当て (Greedy Assignment)
    # 最終的な重心配置に基づき、各クラスターがちょうどK個になるように割り振る
    
    candidates = []
    for i in range(N):
        ax, ay = atoms[i]['x'], atoms[i]['y']
        for cid in range(M):
            cx, cy = centroids[cid]
            d2 = calc_torus_dist_sq(ax, ay, cx, cy, L)
            candidates.append((d2, i, cid))
    
    candidates.sort(key=lambda x: x[0])
    
    atom_target_group = [-1] * N
    cluster_counts = [0] * M
    assigned_count = 0
    
    for _, atom_idx, cid in candidates:
        if assigned_count == N: break
        
        if atom_target_group[atom_idx] != -1: continue
        if cluster_counts[cid] >= K: continue
        
        atom_target_group[atom_idx] = cid
        cluster_counts[cid] += 1
        assigned_count += 1
        components[atom_idx].target_group_id = cid

    # 現在アクティブなコンポーネントのみを保持するリスト
    active_components = components[:]

    # 出力バッファ
    operations = []

    # --- シミュレーションループ (t = 0 to T-1) ---
    for t in range(T):
        
        # 今回結合したペアを記録して、同ターンに重複操作しないようにする
        merged_indices = set()
        next_active_components = []
        
        # --- 貪欲法改: 速攻結合モード ---
        # 距離の閾値を撤廃し、グループ内で可能な限りペアを作って即座に結合させる。
        # 1ターンに各成分は1回しか結合できないが、異なるペア(A-B, C-D)は同時に結合可能とする。
        
        # グループごとにコンポーネントを分類
        groups = {}
        for c in active_components:
            # 前のターンで生成されたが、このターンまだ処理されていないもの
            gid = c.target_group_id
            if gid not in groups: groups[gid] = []
            groups[gid].append(c)
            
        processed_in_this_step = set()
        
        for gid, members in groups.items():
            # このグループ内で、結合可能なペアを貪欲に探し続ける
            # processed_in_this_step に入っていないメンバーだけで考える
            
            # リストをコピーして作業用にする
            available = [m for m in members]
            
            while len(available) >= 2:
                # このグループ内で最も近いペアを探す
                best_pair = None
                min_d2 = float('inf')
                best_indices = (-1, -1)
                
                n_avail = len(available)
                
                for i in range(n_avail):
                    for j in range(i + 1, n_avail):
                        c1 = available[i]
                        c2 = available[j]
                        
                        # サイズチェック (K=30を超えないように)
                        if c1.size() + c2.size() > K:
                            continue

                        d2 = calc_torus_dist_sq(c1.x, c1.y, c2.x, c2.y, L)
                        
                        if d2 < min_d2:
                            min_d2 = d2
                            best_pair = (c1, c2)
                            best_indices = (i, j)
                
                # ペアが見つかれば即結合（閾値なし）
                if best_pair:
                    c1, c2 = best_pair
                    idx1, idx2 = best_indices
                    
                    # --- 結合処理 ---
                    atom_i = c1.atom_indices[0]
                    atom_j = c2.atom_indices[0]
                    operations.append(f"{t} {atom_i} {atom_j}")
                    
                    # 新しいコンポーネントの状態計算
                    new_size = c1.size() + c2.size()
                    new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
                    new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
                    
                    new_c = Component(
                        c_id=atom_i,
                        atom_indices=c1.atom_indices + c2.atom_indices,
                        x=c1.x, y=c1.y,
                        vx=new_vx, vy=new_vy
                    )
                    new_c.target_group_id = gid
                    
                    # 処理済みとしてマーク
                    processed_in_this_step.add(c1)
                    processed_in_this_step.add(c2)
                    
                    # 次のステップ用リストに追加
                    next_active_components.append(new_c)
                    
                    # availableリストから削除 (後ろのインデックスから削除することでズレを防ぐ)
                    available.pop(idx2)
                    available.pop(idx1)
                    
                else:
                    # このグループ内ではもう結合できるペアがない
                    break
            
        # 結合しなかったものはそのまま次へ
        for c in active_components:
            if c not in processed_in_this_step:
                next_active_components.append(c)
        
        active_components = next_active_components

        # --- 移動フェーズ ---
        # 全コンポーネントの位置を更新
        for c in active_components:
            c.x = (c.x + c.vx) % L
            c.y = (c.y + c.vy) % L

    # --- 結果出力 ---
    for op in operations:
        print(op)

if __name__ == "__main__":
    solve()