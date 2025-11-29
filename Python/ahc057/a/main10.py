import sys
import math
import heapq
import random
import time

# --- 定数 ---
# 焼きなまし法の制限時間 (全体)
SA_TIME_LIMIT = 1.7
# 1グループあたりの時間 (均等割り)
PER_GROUP_TIME = 0.15

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

# --- クラス定義 ---

class Atom:
    def __init__(self, aid, x, y, vx, vy):
        self.id = aid
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

# --- グループ最適化ソルバー ---

def solve_group_optimization(group_atoms, T, L, time_limit):
    """
    1つのグループ（30個の原子）に対して、結合タイミングを最適化する。
    
    Args:
        group_atoms: List of Atom objects
        T, L: 問題設定
        time_limit: 実行制限時間
        
    Returns:
        List of operations strings ["t i j", ...]
    """
    K = len(group_atoms)
    start_time = time.time()
    
    # 原子リストをID順などで固定（インデックスアクセス用）
    # ただし、seed（最初にグループの基準となる原子）を決める必要がある。
    # ここでは仮に group_atoms[0] をシード（ベース）とする。
    # 最適化対象は group_atoms[1:] の結合時刻。
    
    # 状態: 各原子の結合時刻 (0 ~ T-1)
    # 初期解: 全員 T-1 で結合 (MST初期解に近い状態)
    # ベース原子(index 0)は時刻0から存在するとみなす（結合操作は発生しない）
    
    # target_times[i] = 原子iがグループに合流する時刻
    # i=0 (Seed) は使わないが便宜上 0 にしておく
    target_times = [T - 1] * K
    target_times[0] = 0 
    
    best_times = list(target_times)
    best_score = float('inf')
    best_ops = []
    
    # 評価関数 (Simulation)
    def evaluate(current_times):
        # (時刻, 原子index) のイベントリスト作成
        # index 0 は最初からいるのでイベントには含めない
        events = []
        for i in range(1, K):
            t = current_times[i]
            # 時刻は 0 <= t < T
            t = max(0, min(t, T - 1))
            events.append((t, i))
        
        # 時刻順にソート
        events.sort()
        
        # シミュレーション状態
        # ベース（現在の塊）の状態
        # 位置は「代表点（シード原子）」の座標で管理し、
        # 他の原子は代表点からの相対座標(offsets)で管理する。
        
        # シード原子の初期状態
        seed = group_atoms[0]
        curr_x = float(seed.x)
        curr_y = float(seed.y)
        curr_vx = float(seed.vx)
        curr_vy = float(seed.vy)
        last_update_t = 0
        
        # グループに含まれる原子の相対座標リスト [(dx, dy), ...]
        # 代表点自身は (0, 0)
        relative_offsets = [(0.0, 0.0)]
        
        total_cost = 0
        ops = []
        
        # 現在の質量（原子数）
        current_size = 1
        
        for t, atom_idx in events:
            atom = group_atoms[atom_idx]
            
            # 1. 時間を進める (last_update_t -> t)
            dt = t - last_update_t
            curr_x = (curr_x + curr_vx * dt) % L
            curr_y = (curr_y + curr_vy * dt) % L
            
            # 2. 結合対象の原子の位置計算 (t時点)
            # 結合前なので等速直線運動
            ax = (atom.x + atom.vx * t) % L
            ay = (atom.y + atom.vy * t) % L
            
            # 3. コスト計算: グループ内の原子の中で一番近いものとの距離
            min_dist = float('inf')
            nearest_offset_idx = -1
            
            # グループ内の全原子（相対座標）を展開してチェック
            # トーラス距離に注意
            for ro_x, ro_y in relative_offsets:
                # グループ内原子の絶対座標
                gx = (curr_x + ro_x) % L
                gy = (curr_y + ro_y) % L
                
                d2 = calc_torus_dist_sq(ax, ay, gx, gy, L)
                if d2 < min_dist:
                    min_dist = d2
                    # 結合相手として記録するのは representative ではなく
                    # 実際に近かった原子のIDが良い？ -> 問題文「点iと点jを結合」
                    # しかしコード上では relative_offsets のインデックスと原子IDの対応が必要
                    # ここでは簡易シミュレーションなのでコストだけ計算し、
                    # 出力時に「代表点と結合」としてもコストは同じ（Dの式は座標依存）。
                    # ただし、厳密には「出力するi, j」の座標で計算される。
                    # ここでは「一番近い原子と結合する」と仮定してコスト算出。
                    pass
            
            total_cost += round(min_dist)
            
            # 操作ログ: 代表点(seed)と結合する形で出力しておく
            # ※実際には一番近い原子IDを指定すべきだが、管理が複雑になるため
            #   ここではseed(id=0の原子)と結合するように記述する。
            #   問題の仕様上、同じ連結成分内なら誰を指定しても結果（速度・位置）は同じ。
            #   結合コストDの計算だけが「指定した2点の距離」依存。
            #   ★重要: コストを最小化するには、出力でも「一番近い原子」を指定する必要がある。
            #   そのためには relative_offsets に対応する原子IDを覚えておく必要がある。
            
            # 簡易実装: コスト計算は正しく行い、出力はseed固定にしてしまうとスコア計算とズレる。
            # なので、後で出力を作り直すか、ここでIDも管理するか。
            # -> ここではID管理は省略し、コスト最適化に集中する。出力時のペアは別途Greedyに決める？
            # いや、ここで決めたtに合わせて出力するので、ペアも重要。
            
            # 修正: relative_offsets に (dx, dy, original_atom_id) を保存する
            
            # 4. 結合・状態更新
            # 新しい速度
            new_vx = (current_size * curr_vx + 1 * atom.vx) / (current_size + 1)
            new_vy = (current_size * curr_vy + 1 * atom.vy) / (current_size + 1)
            
            # 相対座標の追加
            # 現在の代表点(curr_x, curr_y)からの相対位置
            # トーラスを考慮した差分 dx, dy を計算
            dx = ax - curr_x
            dy = ay - curr_y
            if dx > L/2: dx -= L
            elif dx < -L/2: dx += L
            if dy > L/2: dy -= L
            elif dy < -L/2: dy += L
            
            # 新しい原子をメンバーに追加 (dx, dy)
            # ※注意: 速度が変わっても、既存メンバー間の相対位置は変わらない。
            # ただし、座標系は代表点中心。
            relative_offsets.append((dx, dy))
            
            curr_vx = new_vx
            curr_vy = new_vy
            current_size += 1
            last_update_t = t
            
            # 操作リスト (t, atom_id, target_id)
            # ここでは target_id は seed (group_atoms[0].id) とする
            # ★改善: 本来は min_dist を出した相手のIDを入れるべき
            ops.append(f"{t} {atom.id} {seed.id}")
            
        return total_cost, ops

    # evaluateの修正版: ちゃんとIDも管理する
    def evaluate_exact(current_times):
        events = []
        for i in range(1, K):
            t = current_times[i]
            t = max(0, min(t, T - 1))
            events.append((t, i))
        events.sort()
        
        seed = group_atoms[0]
        curr_x, curr_y = float(seed.x), float(seed.y)
        curr_vx, curr_vy = float(seed.vx), float(seed.vy)
        last_update_t = 0
        
        # (dx, dy, atom_id)
        members = [(0.0, 0.0, seed.id)]
        
        total_cost = 0
        ops_log = []
        current_size = 1
        
        for t, atom_idx in events:
            atom = group_atoms[atom_idx]
            dt = t - last_update_t
            curr_x = (curr_x + curr_vx * dt) % L
            curr_y = (curr_y + curr_vy * dt) % L
            
            ax = (atom.x + atom.vx * t) % L
            ay = (atom.y + atom.vy * t) % L
            
            # 最近傍探索
            min_dist = float('inf')
            best_target_id = -1
            
            # メンバ数が増えるとここがボトルネックになる(30回ループ) -> 許容範囲
            for mx, my, mid in members:
                gx = (curr_x + mx) % L
                gy = (curr_y + my) % L
                d2 = calc_torus_dist_sq(ax, ay, gx, gy, L)
                if d2 < min_dist:
                    min_dist = d2
                    best_target_id = mid
            
            total_cost += round(min_dist)
            ops_log.append(f"{t} {atom.id} {best_target_id}")
            
            new_vx = (current_size * curr_vx + atom.vx) / (current_size + 1)
            new_vy = (current_size * curr_vy + atom.vy) / (current_size + 1)
            
            dx = ax - curr_x
            dy = ay - curr_y
            if dx > L/2: dx -= L
            elif dx < -L/2: dx += L
            if dy > L/2: dy -= L
            elif dy < -L/2: dy += L
            
            members.append((dx, dy, atom.id))
            curr_vx = new_vx
            curr_vy = new_vy
            current_size += 1
            last_update_t = t
            
        return total_cost, ops_log

    # 初期評価
    best_score, best_ops = evaluate_exact(best_times)
    
    # 焼きなまし / 山登り
    # 時間いっぱい回す
    loop_cnt = 0
    while time.time() - start_time < time_limit:
        loop_cnt += 1
        
        # 近傍: 1つの原子の時刻を変更
        idx = random.randint(1, K-1) # seed(0)以外
        old_t = target_times[idx]
        
        # 変更幅: ランダム or 少しずらす
        # 全域探索も重要なので、大きく変える操作も入れる
        if random.random() < 0.3:
            new_t = random.randint(0, T - 1)
        else:
            delta = random.randint(-100, 100)
            new_t = max(0, min(T - 1, old_t + delta))
            
        if new_t == old_t: continue
        
        target_times[idx] = new_t
        
        # 評価
        # 部分更新も可能だが、実装量に対しK=30なら全計算で十分速い
        score, ops = evaluate_exact(target_times)
        
        # 採用判定 (単純な山登り + 稀に悪化許容の簡易SA)
        diff = score - best_score
        
        # 温度
        remain = time_limit - (time.time() - start_time)
        temp = 5000 * (remain / time_limit)
        
        if diff < 0 or (temp > 0 and random.random() < math.exp(-diff / temp)):
            # 更新
            if score < best_score:
                best_score = score
                best_ops = ops
                best_times = list(target_times)
            # 現在の状態(target_times)はそのまま維持
        else:
            # 戻す
            target_times[idx] = old_t
            
    return best_ops

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
    # 最終位置の計算
    last_t = T - 1
    for i in range(N):
        x, y, vx, vy = map(int, input().split())
        fx = (x + vx * last_t) % L
        fy = (y + vy * last_t) % L
        atoms.append(Atom(i, x, y, vx, vy))
        atoms[-1].fx = fx
        atoms[-1].fy = fy

    all_operations = []
    used = [False] * N
    random.seed(42)
    
    # グループ割り当てを確定させる (T-1でのGreedy/MST)
    # ここでは単純に「未所属の中でランダムな核に近い29個」を選んで1グループとする
    # これを10回繰り返す
    
    groups = []
    
    for _ in range(M):
        available_indices = [i for i in range(N) if not used[i]]
        if not available_indices: break
        
        # 核選択
        seed_idx = random.choice(available_indices)
        seed_atom = atoms[seed_idx]
        
        # 距離順
        candidates = []
        for idx in available_indices:
            atom = atoms[idx]
            d2 = calc_torus_dist_sq(seed_atom.fx, seed_atom.fy, atom.fx, atom.fy, L)
            candidates.append((d2, idx))
        
        candidates.sort(key=lambda x: x[0])
        cluster_indices = [x[1] for x in candidates[:K]]
        
        for idx in cluster_indices:
            used[idx] = True
            
        group_atom_objs = [atoms[idx] for idx in cluster_indices]
        groups.append(group_atom_objs)

    # 各グループごとに最適化実行
    # 時間配分
    
    for g in groups:
        ops = solve_group_optimization(g, T, L, PER_GROUP_TIME)
        all_operations.extend(ops)

    # 結果出力
    # 時刻順ソート
    parsed_ops = []
    for op_str in all_operations:
        t = int(op_str.split()[0])
        parsed_ops.append((t, op_str))
        
    parsed_ops.sort(key=lambda x: x[0])
    
    for _, op_str in parsed_ops:
        print(op_str)

if __name__ == "__main__":
    solve()