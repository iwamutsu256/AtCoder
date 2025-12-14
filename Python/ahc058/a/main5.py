import sys

def solve():
    # --- 1. 高速入力と1次元化 ---
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    L = int(next(iterator))
    T = int(next(iterator))
    K = int(next(iterator))
    
    # 1次元配列として読み込む
    # A: [A0, A1, ..., A9]
    A = [int(next(iterator)) for _ in range(N)]
    
    # C: [C_0_0, ..., C_3_9] (40個)
    # P: [P_0_0, ..., P_3_9] (40個)
    # B: [B_0_0, ..., B_3_9] (40個)
    C = [int(next(iterator)) for _ in range(N * L)]
    P = [0] * (N * L)
    B = [1] * (N * L)
    
    # 配列アクセスのためのインデックス定数（高速化用）
    # Level 0, 1, 2, 3 の開始インデックス
    IDX_L0 = 0
    IDX_L1 = N
    IDX_L2 = N * 2
    IDX_L3 = N * 3
    RANGE_N = range(N) # 毎回 range(N) を作るコストを削減

    current_apples = K

    # --- 2. メインループ ---
    for t in range(T):
        best_score = -1
        best_action = -1 # -1: 何もしない, 0~39: そのIDの機械を強化
        
        # 残りターン数
        remaining_turns = T - 1 - t
        
        # --- 候補の選定 ---
        # 1. 何もしない (必ず候補)
        # 2. 現在のお金で買える機械 (全て候補)
        
        # 「何もしない」場合のシミュレーション
        # ベースラインとして計算
        
        # シミュレーション用変数の準備
        # Bは変化するのでコピーが必要
        sim_B_base = list(B)
        score_base = current_apples
        
        # シミュレーションループ (何もしない版)
        # 高速化のため、ここに関数呼び出しは使わない
        sim_apples = score_base
        sim_B = list(sim_B_base)
        
        # LevelごとのPキャッシュ (このターンPは不変)
        # 毎回配列アクセスするより、ローカル変数にしたほうが速い可能性があるが
        # N=10なのでループ内でアクセスしても許容範囲
        
        # --- 高速シミュレーション (展開版) ---
        for _ in range(remaining_turns + 1):
            # Level 0 生産
            prod = 0
            for j in RANGE_N:
                # P[j] > 0 チェックはあえてしない（分岐コスト削減のため単純計算）
                prod += A[j] * sim_B[j] * P[j]
            sim_apples += prod
            
            # Level 1 -> 0
            for j in RANGE_N:
                sim_B[j] += sim_B[IDX_L1 + j] * P[IDX_L1 + j]
            # Level 2 -> 1
            for j in RANGE_N:
                sim_B[IDX_L1 + j] += sim_B[IDX_L2 + j] * P[IDX_L2 + j]
            # Level 3 -> 2
            for j in RANGE_N:
                sim_B[IDX_L2 + j] += sim_B[IDX_L3 + j] * P[IDX_L3 + j]
        
        best_score = sim_apples
        best_action = -1
        
        # --- 「強化する」候補の探索 ---
        # 全40個を見るが、コスト不足は即スキップ
        for idx in range(N * L):
            # コスト計算
            # P[idx] はリストアクセス
            cost = C[idx] * (P[idx] + 1)
            
            if cost > current_apples:
                continue
            
            # 買える場合: シミュレーション実行
            # 初期状態
            sim_apples = current_apples - cost
            sim_B = list(B) # Bはリセット
            
            # Pは一時的に +1 されたとして計算
            # 配列を書き換えると遅いので、計算式の中で +1 するか
            # あるいは P_temp を作るか。
            # ここでは「どの Level の機械か」で分岐してループを回す
            
            # ターゲットのLevelとID
            target_lvl = idx // N
            target_id = idx % N
            
            # シミュレーションループ
            for _ in range(remaining_turns + 1):
                # Level 0 生産
                prod = 0
                for j in RANGE_N:
                    p_val = P[j]
                    if target_lvl == 0 and j == target_id:
                        p_val += 1
                    prod += A[j] * sim_B[j] * p_val
                sim_apples += prod
                
                # Level 1 -> 0
                for j in RANGE_N:
                    p_val = P[IDX_L1 + j]
                    if target_lvl == 1 and j == target_id:
                        p_val += 1
                    sim_B[j] += sim_B[IDX_L1 + j] * p_val
                    
                # Level 2 -> 1
                for j in RANGE_N:
                    p_val = P[IDX_L2 + j]
                    if target_lvl == 2 and j == target_id:
                        p_val += 1
                    sim_B[IDX_L1 + j] += sim_B[IDX_L2 + j] * p_val
                    
                # Level 3 -> 2
                for j in RANGE_N:
                    p_val = P[IDX_L3 + j]
                    if target_lvl == 3 and j == target_id:
                        p_val += 1
                    sim_B[IDX_L2 + j] += sim_B[IDX_L3 + j] * p_val
            
            # スコア比較
            if sim_apples > best_score:
                best_score = sim_apples
                best_action = idx
        
        # --- 行動実行 ---
        if best_action != -1:
            # 強化
            cost = C[best_action] * (P[best_action] + 1)
            current_apples -= cost
            P[best_action] += 1
            
            # 出力 (1次元 -> 2次元)
            act_i = best_action // N
            act_j = best_action % N
            print(f"{act_i} {act_j}")
        else:
            print("-1")
            
        # --- 実際のターン経過処理 ---
        # Level 0 生産
        prod = 0
        for j in RANGE_N:
            prod += A[j] * B[j] * P[j]
        current_apples += prod
        
        # Level 1 -> 0
        for j in RANGE_N:
            B[j] += B[IDX_L1 + j] * P[IDX_L1 + j]
        # Level 2 -> 1
        for j in RANGE_N:
            B[IDX_L1 + j] += B[IDX_L2 + j] * P[IDX_L2 + j]
        # Level 3 -> 2
        for j in RANGE_N:
            B[IDX_L2 + j] += B[IDX_L3 + j] * P[IDX_L3 + j]

    sys.stdout.flush()

if __name__ == "__main__":
    solve()