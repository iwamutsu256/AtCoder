import sys

def solve():
    # --- 1. 高速入力 ---
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    L = int(next(iterator))
    T = int(next(iterator))
    K = int(next(iterator))
    
    A = [int(next(iterator)) for _ in range(N)]
    
    # 1次元配列化
    C = [int(next(iterator)) for _ in range(N * L)]
    P = [0] * (N * L)
    B = [1] * (N * L)
    
    # 定数 (インデックス計算用)
    IDX_L1 = N
    IDX_L2 = N * 2
    IDX_L3 = N * 3
    
    RANGE_N = range(N)
    RANGE_ALL = range(N * L)

    current_apples = K

    # --- 2. メインループ ---
    for t in range(T):
        remaining_turns = T - 1 - t
        
        # --- A. ターゲット（目標）の動的決定 ---
        # Cost Efficiency (効率) が最も高い機械を探す
        # 効率 = (A[j] * Levelの重み) / 現在のコスト
        # シミュレーションせずに数式で瞬時に計算する
        
        best_target_idx = -1
        max_efficiency = -1.0
        
        # 重み係数 (残りターン R に応じた各レベルの強さ)
        # R, R^2, R^3, R^4 の比率を使う
        R = remaining_turns
        if R > 0:
            weights = [
                R,              # Level 0
                R**2 / 2,       # Level 1
                R**3 / 6,       # Level 2
                R**4 / 24       # Level 3
            ]
        else:
            weights = [0, 0, 0, 0]

        for idx in range(N * L):
            level = idx // N
            j = idx % N
            
            # 現在のコスト
            cost = C[idx] * (P[idx] + 1)
            
            # 効率計算
            # ゼロ除算回避のため cost は必ず 1以上 (問題制約でC>=1)
            efficiency = (A[j] * weights[level]) / cost
            
            if efficiency > max_efficiency:
                max_efficiency = efficiency
                best_target_idx = idx
        
        # ターゲットが決まった
        target_idx = best_target_idx
        
        # --- B. 行動選択 (シミュレーション) ---
        # 「ターゲットをいつ買うか？」を軸に、今の行動を決める
        
        best_score = -1
        best_action = -1 # -1: 貯金
        
        # 候補: -1 と、今買えるもの
        candidates = [-1] + [i for i in RANGE_ALL if C[i] * (P[i] + 1) <= current_apples]
        
        for action in candidates:
            sim_apples = current_apples
            sim_B = list(B)
            
            # Pはコピーせず、actionとtargetだけ特別扱いして高速化
            # シミュレーション中のPの増分を管理する辞書（またはフラグ）
            # action と target は同じ可能性もあるので注意
            
            p_add = {} # idx -> increment value
            
            # アクション実行
            if action != -1:
                cost = C[action] * (P[action] + 1)
                sim_apples -= cost
                p_add[action] = p_add.get(action, 0) + 1
            
            # シミュレーション内でターゲットを買ったかフラグ
            bought_target = False
            
            # もし今回のアクションがターゲットそのものなら、購入済み扱い
            if action == target_idx:
                bought_target = True
            
            # --- 高速シミュレーションループ ---
            for _ in range(remaining_turns + 1):
                # 1. ターゲット購入判定
                if not bought_target:
                    # ターゲットの現在のコスト (P + シミュレーション内の増加分)
                    curr_p = P[target_idx] + p_add.get(target_idx, 0)
                    curr_target_cost = C[target_idx] * (curr_p + 1)
                    
                    if sim_apples >= curr_target_cost:
                        sim_apples -= curr_target_cost
                        p_add[target_idx] = p_add.get(target_idx, 0) + 1
                        bought_target = True
                
                # 2. 生産処理
                # Pの値解決を高速化: p_add にあるなら足す、なければそのまま
                # dict.get は遅いので、必要な変数を用意しておく
                
                # p_add は最大でも2要素 (actionとtarget) なので、
                # ループ内で毎回チェックしてもそこまで遅くないが、展開する
                
                act_idx = action if action != -1 else -999
                tgt_idx = target_idx if bought_target else -999
                
                # Level 0
                prod = 0
                for j in RANGE_N:
                    p_val = P[j]
                    # 該当するなら加算
                    if j == act_idx: p_val += 1
                    if j == tgt_idx: p_val += 1 # action==targetならここで+2になるが、上記ロジックでboughtならactionと重複しないようにすべき
                    
                    # 修正: bought_targetフラグがTrueになった瞬間、tgt_idxが有効になる。
                    # actionとtargetが同じ場合:
                    #   action実行時: p_add[target] = 1. act_idx=target.
                    #   bought判定: True. tgt_idx=target.
                    #   これだと +2 されてしまう。
                    #   => p_add を正として使うのが安全。
                    
                    # p_add を使う方式に統一
                    # しかしdictは遅い。
                    # 配列アクセスの方が速いので、p_add 配列を作る？ -> 40要素なら一瞬
                    
                # 高速化のため書き直し: sim_P 配列を作る (40要素コピーは速い)
                pass # 下のブロックで実装し直します
            
            # --- シミュレーション実装（やり直し） ---
            # ループ前の準備
            sim_P = list(P)
            if action != -1:
                sim_P[action] += 1
            
            bought_target_in_sim = False
            if action == target_idx:
                bought_target_in_sim = True
            
            for _ in range(remaining_turns + 1):
                # ターゲット購入トライ
                if not bought_target_in_sim:
                    t_cost = C[target_idx] * (sim_P[target_idx] + 1)
                    if sim_apples >= t_cost:
                        sim_apples -= t_cost
                        sim_P[target_idx] += 1
                        bought_target_in_sim = True
                
                # 生産
                # Level 0
                prod = 0
                for j in RANGE_N:
                    # P[j] > 0 チェック省略 (分岐減らし)
                    prod += A[j] * sim_B[j] * sim_P[j]
                sim_apples += prod
                
                # Level 1 -> 0
                for j in RANGE_N:
                    sim_B[j] += sim_B[IDX_L1 + j] * sim_P[IDX_L1 + j]
                # Level 2 -> 1
                for j in RANGE_N:
                    sim_B[IDX_L1 + j] += sim_B[IDX_L2 + j] * sim_P[IDX_L2 + j]
                # Level 3 -> 2
                for j in RANGE_N:
                    sim_B[IDX_L2 + j] += sim_B[IDX_L3 + j] * sim_P[IDX_L3 + j]
            
            if sim_apples > best_score:
                best_score = sim_apples
                best_action = action
        
        # --- 行動実行 ---
        if best_action != -1:
            # 1次元 -> 2次元
            print(f"{best_action // N} {best_action % N}")
            cost = C[best_action] * (P[best_action] + 1)
            current_apples -= cost
            P[best_action] += 1
        else:
            print("-1")
            
        # --- ターン経過 ---
        prod = 0
        for j in RANGE_N:
            prod += A[j] * B[j] * P[j]
        current_apples += prod
        
        for j in RANGE_N:
            B[j] += B[IDX_L1 + j] * P[IDX_L1 + j]
        for j in RANGE_N:
            B[IDX_L1 + j] += B[IDX_L2 + j] * P[IDX_L2 + j]
        for j in RANGE_N:
            B[IDX_L2 + j] += B[IDX_L3 + j] * P[IDX_L3 + j]

    sys.stdout.flush()

if __name__ == "__main__":
    solve()