import sys
import time
import random
import math

# グローバル定数 (入力読み込み後に設定)
N, L, T, K = 0, 0, 0, 0
A = []
C = []

def solve():
    """
    AHC問題「Apple Incremental Game」に対する焼きなまし法ソルバー。

    【アルゴリズム概要】
    1. 初期解生成:
       - 既存の貪欲法 (ID=0優先 + 資金稼ぎLevel0) を実行し、その操作手順を初期解とする。
    2. 焼きなまし法 (Simulated Annealing):
       - 状態: 購入する機械の順序リスト [(level, id), ...]
       - 評価関数: Tターン終了時点のスコア (round(10^5 * log2(apples)))
       - 近傍操作:
         - 削除 (Delete): ランダムに1つの操作を取り除く
         - 追加 (Add): ランダムな位置に有効な操作を追加する
         - 交換 (Swap): リスト内の2つの操作順序を入れ替える
       - 遷移: 500ターン以内でシミュレーションを行い、スコアが良ければ採用。悪くても確率で採用。
    3. 最終出力:
       - 最良の操作リストに基づいてシミュレーションを行い、各ターンの行動を出力する。
    """
    global N, L, T, K, A, C

    # --- 入力の読み込み ---
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N, L, T, K = map(int, line1)

        A = list(map(int, sys.stdin.readline().split()))

        C = []
        for _ in range(L):
            C.append(list(map(int, sys.stdin.readline().split())))

    except ValueError:
        return

    # --- 時間計測開始 ---
    start_time = time.time()
    TIME_LIMIT = 1.8  # 制限時間 (秒)

    # ---------------------------------------------------------
    # 1. 初期解の生成 (貪欲法ベース)
    # ---------------------------------------------------------
    initial_ops = get_initial_greedy_solution()
    
    # ---------------------------------------------------------
    # 2. 焼きなまし法 (Simulated Annealing)
    # ---------------------------------------------------------
    
    # 現在の状態
    current_ops = list(initial_ops)
    current_score = simulate(current_ops)
    
    # 最良の状態
    best_ops = list(current_ops)
    best_score = current_score
    
    # 温度パラメータ
    temp_start = 2000.0
    temp_end = 100.0
    
    # ループカウンタ (デバッグ/調整用)
    iter_count = 0
    
    while True:
        # 時間チェック
        now = time.time()
        if now - start_time > TIME_LIMIT:
            break
        
        iter_count += 1
        
        # 温度の更新 (線形冷却)
        progress = (now - start_time) / TIME_LIMIT
        temp = temp_start + (temp_end - temp_start) * progress
        
        # --- 近傍操作 ---
        # 0: Delete, 1: Add, 2: Swap
        mode = random.randint(0, 2)
        
        # 近傍適用後の新しい操作リストを作成
        new_ops = list(current_ops)
        
        if mode == 0: # Delete
            if len(new_ops) > 0:
                idx = random.randint(0, len(new_ops) - 1)
                new_ops.pop(idx)
            else:
                # 空の場合は何もしない (スキップ)
                continue
                
        elif mode == 1: # Add
            # 挿入位置
            idx = random.randint(0, len(new_ops))
            
            # 追加する操作の候補を作成
            # ID=0 は全Level, ID!=0 は Level 0 のみ (生産効率のため)
            if random.random() < 0.3:
                # 30%の確率で ID!=0 の Level 0 を追加 (資金稼ぎ強化)
                add_id = random.randint(1, N - 1)
                add_level = 0
            else:
                # 70%の確率で ID=0 のいずれかの Level を追加
                add_id = 0
                add_level = random.randint(0, L - 1)
                
            new_ops.insert(idx, (add_level, add_id))
            
        elif mode == 2: # Swap
            if len(new_ops) >= 2:
                idx1 = random.randint(0, len(new_ops) - 1)
                idx2 = random.randint(0, len(new_ops) - 1)
                new_ops[idx1], new_ops[idx2] = new_ops[idx2], new_ops[idx1]
            else:
                continue

        # --- 評価 ---
        new_score = simulate(new_ops)
        
        # --- 遷移判定 ---
        # スコアは大きい方が良い
        delta = new_score - current_score
        
        if delta >= 0:
            # 改善した場合は必ず採用
            current_ops = new_ops
            current_score = new_score
            
            # ベスト更新
            if new_score > best_score:
                best_score = new_score
                best_ops = list(new_ops)
        else:
            # 悪化した場合も確率で採用
            # delta は負の値。temp が大きいほど採用しやすい。
            # スコアの変動幅が大きいので、スケーリングが必要かも知れないが、
            # ログスコア自体はおおよそ数千〜数万のオーダー。
            # ここではシンプルに判定。
            prob = math.exp(delta / temp)
            if random.random() < prob:
                current_ops = new_ops
                current_score = new_score

    # ---------------------------------------------------------
    # 3. 最終出力
    # ---------------------------------------------------------
    # 最良の操作リストで再シミュレーションし、行動を出力
    simulate(best_ops, output_mode=True)


def get_initial_greedy_solution():
    """
    初期解として、既存の貪欲法による操作リストを生成する。
    """
    ops = []
    
    # 状態変数の初期化 (ローカル変数として)
    current_apples = K
    B = [[1] * N for _ in range(L)]
    P = [[0] * N for _ in range(L)]
    
    for t in range(T):
        action_i = -1
        action_j = -1
        
        found_high_level = False
        target_id = 0
        
        # 戦略A: ID=0 の高レベル (Level 1, 2, 3)
        for i in range(L - 1, 0, -1):
            cost = C[i][target_id] * (P[i][target_id] + 1)
            if current_apples >= cost:
                action_i = i
                action_j = target_id
                
                current_apples -= cost
                P[i][target_id] += 1
                found_high_level = True
                break
        
        # 戦略B: Level 0 でコスパ最強を探す
        if not found_high_level:
            best_efficiency = -1.0
            best_j = -1
            
            for j in range(N):
                cost = C[0][j] * (P[0][j] + 1)
                if current_apples < cost:
                    continue
                
                gain = A[j] * B[0][j]
                efficiency = gain / cost
                
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_j = j
            
            if best_j != -1:
                action_i = 0
                action_j = best_j
                
                current_apples -= cost
                P[0][best_j] += 1

        # 操作があった場合のみリストに追加
        if action_i != -1:
            ops.append((action_i, action_j))
            
        # 生産シミュレーション
        for i in range(L):
            for j in range(N):
                count = B[i][j]
                power = P[i][j]
                if i == 0:
                    current_apples += A[j] * count * power
                else:
                    B[i-1][j] += count * power
                    
    return ops


def simulate(ops, output_mode=False):
    """
    操作リストに基づいてシミュレーションを行う関数。
    
    Args:
        ops (list): 操作手順のリスト [(level, id), ...]
        output_mode (bool): Trueの場合、標準出力に行動を出力する。

    Returns:
        int: スコア (round(10^5 * log2(apples)))
    """
    # 高速化のため、1次元配列を使用
    # インデックス計算: idx = i * N + j
    
    current_apples = K
    B = [1] * (N * L)  # 個数
    P = [0] * (N * L)  # パワー
    
    op_idx = 0
    num_ops = len(ops)
    
    # 毎ターンの生産計算用の一時変数
    # A配列もアクセスしやすいようにしておく
    local_A = A
    local_N = N
    local_L = L
    local_C = C # 2次元のままアクセス (C[i][j])
    
    # ターンループ
    for t in range(T):
        
        # --- 行動決定フェーズ ---
        act_i = -1
        act_j = -1
        
        # リストにまだ操作が残っているなら、次を実行できるか試す
        if op_idx < num_ops:
            target_i, target_j = ops[op_idx]
            idx = target_i * local_N + target_j
            
            # コスト計算
            # Cは初期化で読み込んでいるグローバル(またはローカル参照)
            cost = local_C[target_i][target_j] * (P[idx] + 1)
            
            if current_apples >= cost:
                # 購入実行
                current_apples -= cost
                P[idx] += 1
                act_i = target_i
                act_j = target_j
                op_idx += 1
            # else: 買えない場合は「待機」なので何もしない (-1)
        
        if output_mode:
            if act_i != -1:
                print(f"{act_i} {act_j}")
            else:
                print("-1")
        
        # --- 生産フェーズ ---
        # Level 0 (りんご生産)
        # apples += sum(A[j] * B[0][j] * P[0][j])
        # 高速化: ループ展開気味に
        
        # Level 0 の範囲: index 0 〜 N-1
        # B, P は1次元配列
        # production_0 = 0
        for j in range(local_N):
            # idx = j
            # if P[j] > 0: # Pが0なら生産なしだが、分岐コストと比較してそのまま計算
            current_apples += local_A[j] * B[j] * P[j]
        
        # Level 1 〜 L-1 (機械生産)
        # B[i-1][j] += B[i][j] * P[i][j]
        
        # Level 1 (idx N ~ 2N-1) -> Level 0 (idx 0 ~ N-1)
        # Level 2 (idx 2N ~ 3N-1) -> Level 1 (idx N ~ 2N-1)
        # ...
        
        # i = 1 to L-1
        for i in range(1, local_L):
            offset = i * local_N
            prev_offset = (i - 1) * local_N
            for j in range(local_N):
                idx = offset + j
                prev_idx = prev_offset + j
                # P[idx] > 0 のチェックを入れると速くなる可能性があるが、
                # Pythonのループオーバーヘッドが大きいので単純計算
                increase = B[idx] * P[idx]
                if increase > 0:
                    B[prev_idx] += increase

    # スコア計算
    if current_apples <= 0:
        return 0 # エラーケース (通常ありえない)
        
    score = round(100000 * math.log2(current_apples))
    return score

if __name__ == "__main__":
    solve()