import sys
import math

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
    
    # 最初の行: N, T, M, K, L (本問題では固定値だが、念のため読み込む)
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
    # 初期状態では、各原子がそれぞれ独立したコンポーネント
    components = []
    for atom in atoms:
        c = Component(atom['id'], [atom['id']], atom['x'], atom['y'], atom['vx'], atom['vy'])
        components.append(c)

    # --- 戦略: 初期グループ分け (Pre-Clustering) ---
    # 最終的に作るのはサイズK(30)のグループM(10)個。
    # 近いもの同士をくっつけたいので、初期位置のX座標でソートして
    # 30個ずつ「ターゲットグループ」IDを割り振る。
    # これにより、遠く離れた原子同士が結合しようとするのを防ぐ。
    
    # X座標でソートするための補助リスト (index, x)
    sorted_indices = sorted(range(N), key=lambda i: atoms[i]['x'])
    
    # 各原子が「どのグループ(0~9)に属すべきか」を記録する配列
    atom_target_group = [-1] * N
    
    for i in range(N):
        original_idx = sorted_indices[i]
        group_id = i // K  # 0~29 -> 0, 30~59 -> 1, ...
        atom_target_group[original_idx] = group_id
        
        # コンポーネントにも情報を付与
        components[original_idx].target_group_id = group_id

    # 現在アクティブなコンポーネントのみを保持するリスト（ID管理用ではない）
    # 処理の高速化のため、リストから削除していくのではなく、isValidフラグ管理等が望ましいが
    # ここではPythonのリスト操作で管理する。
    active_components = components[:]

    # 出力バッファ
    operations = []

    # --- シミュレーションループ (t = 0 to T-1) ---
    for t in range(T):
        
        # 今回結合したペアを記録して、同ターンに重複操作しないようにする
        merged_indices = set()
        next_active_components = []
        
        # --- 貪欲法: 結合判定 ---
        
        # 戦略: 
        # 1. 同じターゲットグループに属するコンポーネント同士だけを見る
        # 2. 距離が閾値以下なら結合する
        # 3. 閾値はターン経過とともに緩くする（最初は厳選、最後は必死）
        
        # 閾値の計算 (ヒューリスティック係数)
        # 序盤は距離 2000^2 くらいまで、終盤は無制限(L^2)に近づける
        # L=100000 なので、かなり広い。
        progress = t / T
        threshold_dist_sq = (5000 + progress * 80000) ** 2 
        
        # 強引な結合モード（残り時間が少ないのにまだ結合できていない場合）
        if t > T - 100:
            threshold_dist_sq = L**2 * 2  # 無限大
            
        # グループごとにコンポーネントを分類
        groups = {}
        for c in active_components:
            if c.id in merged_indices: continue # 既にこのターンで処理済みならスキップ
            
            gid = c.target_group_id
            if gid not in groups: groups[gid] = []
            groups[gid].append(c)
            
        # 各グループ内でペアを探す
        # ※全探索は重いが、各グループ最大30個(結合済みならもっと少ない)なので計算量は軽い
        processed_in_this_step = set() # このステップで削除される予定のID
        
        for gid, members in groups.items():
            # メンバー数が1なら結合相手がいない
            if len(members) < 2:
                continue
                
            # グループ内で総当たり距離計算し、ベストペアを探す
            # 貪欲法：一番近いペアを1組だけ見つけて結合させる（1ターン1グループ1結合に制限して様子見）
            best_pair = None
            min_d2 = float('inf')
            
            # メンバーリスト内でペア探索
            # membersはComponentオブジェクトのリスト
            n_mem = len(members)
            for i in range(n_mem):
                for j in range(i + 1, n_mem):
                    c1 = members[i]
                    c2 = members[j]
                    
                    # 既に完成形(サイズ30)なら結合しない
                    if c1.size() + c2.size() > K:
                        continue

                    d2 = calc_torus_dist_sq(c1.x, c1.y, c2.x, c2.y, L)
                    
                    if d2 < min_d2:
                        min_d2 = d2
                        best_pair = (c1, c2)
            
            # 閾値チェックして結合
            if best_pair and min_d2 <= threshold_dist_sq:
                c1, c2 = best_pair
                
                # --- 結合処理 ---
                # 1. 出力の記録 (時刻 t, c1の代表元, c2の代表元)
                # 問題文より「出力の順番は任意」だが、元の原子番号を出力する必要がある
                # ここでは「成分iと成分jを結合」とあるが、これは「成分の代表点」ではなく
                # 「成分に含まれる任意の点」を指定すればよいのか？
                # 問題文: "点 i の時刻 t における位置... 点 i と 点 j を結合する"
                # とあるので、各成分に含まれる原子のIDを1つずつ指定すれば良い。
                atom_i = c1.atom_indices[0]
                atom_j = c2.atom_indices[0]
                operations.append(f"{t} {atom_i} {atom_j}")
                
                # 2. 新しいコンポーネントの状態計算 (運動量保存)
                new_size = c1.size() + c2.size()
                
                # 速度更新: 重み付き平均
                new_vx = (c1.size() * c1.vx + c2.size() * c2.vx) / new_size
                new_vy = (c1.size() * c1.vy + c2.size() * c2.vy) / new_size
                
                # 新しいコンポーネントオブジェクト作成
                # 位置はどちらでも良いが、便宜上c1の位置にしておく（結合の瞬間は変わらない）
                # IDは便宜上 atom_i を使う
                new_c = Component(
                    c_id=atom_i,
                    atom_indices=c1.atom_indices + c2.atom_indices,
                    x=c1.x, y=c1.y, # 位置はとりあえずc1のものを継承（このあと移動フェーズで更新）
                    vx=new_vx, vy=new_vy
                )
                new_c.target_group_id = gid # ターゲットグループを引き継ぐ
                
                # 処理済みリストに追加（移動フェーズのために、この新しいCを追加）
                # 元の c1, c2 は active_components から除外扱いにする
                processed_in_this_step.add(c1)
                processed_in_this_step.add(c2)
                
                # 次のループのために追加（ただし位置更新はあとで一括）
                next_active_components.append(new_c)
                
                # 1ターンに1グループ1回のみ結合とすることで、連鎖的な複雑さを回避
                continue

        # 結合しなかったものはそのまま next_active_components へ
        for c in active_components:
            if c not in processed_in_this_step:
                next_active_components.append(c)
        
        # リスト更新
        active_components = next_active_components

        # --- 移動フェーズ ---
        # 全コンポーネントの位置を更新
        for c in active_components:
            c.x = (c.x + c.vx) % L
            c.y = (c.y + c.vy) % L

    # --- 結果出力 ---
    # 結果は結合操作のみを出力する
    for op in operations:
        print(op)

if __name__ == "__main__":
    solve()