import sys

# ==========================================
# 共通処理: スコア評価関数
# 生成された行動リスト(actions)を実行した場合の最終リンゴ数を計算
# ==========================================
def evaluate(N, L, T, K, A, C, actions):
    apples = K
    P = [0] * (N * L)
    B = [1] * (N * L)
    
    IDX_L1 = N
    IDX_L2 = N * 2
    IDX_L3 = N * 3
    RANGE_N = range(N)
    
    for action_str in actions:
        # 1. 行動の実行 (購入)
        if action_str != "-1":
            try:
                r, c = map(int, action_str.split())
                idx = r * N + c
                cost = C[idx] * (P[idx] + 1)
                if apples >= cost:
                    apples -= cost
                    P[idx] += 1
                else:
                    # 資金不足等の場合は購入キャンセル（何もしない扱い）
                    pass 
            except:
                pass

        # 2. 生産・増殖
        prod = 0
        for j in RANGE_N: prod += A[j] * B[j] * P[j]
        apples += prod
        
        # 増殖処理 (依存関係が一方向なので順次更新でOK)
        # B0はB1に依存、B1はB2に依存...
        for j in RANGE_N: B[j] += B[IDX_L1+j] * P[IDX_L1+j]
        for j in RANGE_N: B[IDX_L1+j] += B[IDX_L2+j] * P[IDX_L2+j]
        for j in RANGE_N: B[IDX_L2+j] += B[IDX_L3+j] * P[IDX_L3+j]
        
    return apples

# ==========================================
# 戦略1: ヒューリスティック (Wait & Buy, ピラミッド維持重視)
# 特徴: 長期的な「溜め」や「バランス」を考慮できる
# ==========================================
def solve_heuristic(N, L, T, K, A, C):
    actions = [] # 出力用リスト
    
    P = [0] * (N * L)
    B = [1] * (N * L)
    
    IDX_L1 = N
    IDX_L2 = N * 2
    IDX_L3 = N * 3
    RANGE_N = range(N)
    RANGE_ALL = range(N * L)
    
    current_apples = K
    current_turn = 0
    
    # --- チャンピオンID選定 ---
    best_tower_id = -1
    best_tower_score = -1.0
    for j in range(N):
        cost_sum = C[j] + C[N + j] + C[2*N + j] + C[3*N + j]
        score = A[j] / cost_sum if cost_sum > 0 else 0
        if score > best_tower_score:
            best_tower_score = score
            best_tower_id = j
            
    target_id = best_tower_id
    idx_t0, idx_t1, idx_t2, idx_t3 = target_id, N+target_id, 2*N+target_id, 3*N+target_id
    focused_indices = [idx_t0, idx_t1, idx_t2, idx_t3]

    PHASE_SWITCH_MIN = 130
    PHASE_SWITCH_MAX = 200
    BUY_L2_THRESHOLD = 20

    while current_turn < T:
        remaining_limit = T - current_turn
        current_production = sum(A[j] * B[j] * P[j] for j in RANGE_N)
        
        # フェーズ判定
        is_phase2 = False
        if current_turn >= PHASE_SWITCH_MAX:
            is_phase2 = True
        elif current_turn >= PHASE_SWITCH_MIN:
            cost_l2 = C[idx_t2] * (P[idx_t2] + 1)
            if current_production > 0:
                needed = max(0, cost_l2 - current_apples)
                if needed / current_production <= BUY_L2_THRESHOLD:
                    is_phase2 = True

        best_action = -1
        best_wait_turns = 0
        
        # --- Phase 1: 立ち上げ期 ---
        if not is_phase2:
            best_roi = -1.0
            R = remaining_limit
            weights = [R, R**2/2, R**3/6, R**4/24]
            bias = [10.0, 5.0, 1.0, 0.1]
            
            for idx in RANGE_ALL:
                cost = C[idx] * (P[idx] + 1)
                if cost > current_apples: continue
                
                lvl, j = idx // N, idx % N
                gain = A[j] * weights[lvl] * bias[lvl]
                roi = gain / cost
                if roi > best_roi:
                    best_roi = roi
                    best_action = idx
            best_wait_turns = 0

        # --- Phase 2: 集中投資期 ---
        else:
            # バランスチェック (L3抑制)
            p0, p1, p2, p3 = P[idx_t0], P[idx_t1], P[idx_t2], P[idx_t3]
            forced_target = None
            if p3 >= p0: forced_target = idx_t0
            elif p3 >= p1: forced_target = idx_t1
            elif p3 >= p2: forced_target = idx_t2
            
            candidates = [forced_target] if forced_target is not None else focused_indices
            
            # 即買いチェック
            buyable = [idx for idx in candidates if C[idx]*(P[idx]+1) <= current_apples]
            
            if buyable:
                best_action = forced_target if forced_target is not None else max(buyable, key=lambda x: x//N)
                best_wait_turns = 0
            else:
                # 待機評価 (Wait & Buy)
                best_score = -1.0
                wait_limit = min(remaining_limit, 80)
                
                sim_targets = [forced_target] if forced_target is not None else focused_indices
                
                for idx in sim_targets:
                    cost = C[idx] * (P[idx] + 1)
                    if current_production <= 0: continue
                    
                    # 概算待機ターン
                    approx_wait = int(max(0, cost - current_apples) / current_production)
                    if approx_wait >= wait_limit: continue

                    # 精密待機計算
                    t_apples = current_apples
                    t_B = list(B)
                    found_wait = -1
                    
                    for w in range(wait_limit):
                        if t_apples >= cost:
                            found_wait = w
                            break
                        prod = sum(A[j] * t_B[j] * P[j] for j in RANGE_N)
                        t_apples += prod
                        for j in RANGE_N: t_B[j] += t_B[IDX_L1+j] * P[IDX_L1+j]
                        for j in RANGE_N: t_B[IDX_L1+j] += t_B[IDX_L2+j] * P[IDX_L2+j]
                        for j in RANGE_N: t_B[IDX_L2+j] += t_B[IDX_L3+j] * P[IDX_L3+j]
                    
                    if found_wait == -1 or found_wait + 1 > remaining_limit: continue
                    
                    # 購入後の残りシミュレーション
                    rem_after = remaining_limit - (found_wait + 1)
                    sim_apples = t_apples - cost
                    sim_B_final = list(t_B)
                    tgt_l, tgt_j = idx // N, idx % N
                    
                    # 簡易シミュレーション
                    for _ in range(rem_after):
                        prod = 0
                        for j in RANGE_N:
                            p_val = P[j] + (1 if tgt_l==0 and j==tgt_j else 0)
                            prod += A[j] * sim_B_final[j] * p_val
                        sim_apples += prod
                        for j in RANGE_N:
                            p_val = P[IDX_L1+j] + (1 if tgt_l==1 and j==tgt_j else 0)
                            sim_B_final[j] += sim_B_final[IDX_L1+j] * p_val
                        for j in RANGE_N:
                            p_val = P[IDX_L2+j] + (1 if tgt_l==2 and j==tgt_j else 0)
                            sim_B_final[IDX_L1+j] += sim_B_final[IDX_L2+j] * p_val
                        for j in RANGE_N:
                            p_val = P[IDX_L3+j] + (1 if tgt_l==3 and j==tgt_j else 0)
                            sim_B_final[IDX_L2+j] += sim_B_final[IDX_L3+j] * p_val
                            
                    if sim_apples > best_score:
                        best_score = sim_apples
                        best_action = idx
                        best_wait_turns = found_wait

        # --- 行動適用 ---
        # 待機実行
        if best_wait_turns > 0:
            for _ in range(best_wait_turns):
                actions.append("-1")
                prod = sum(A[j] * B[j] * P[j] for j in RANGE_N)
                current_apples += prod
                for j in RANGE_N: B[j] += B[IDX_L1+j] * P[IDX_L1+j]
                for j in RANGE_N: B[IDX_L1+j] += B[IDX_L2+j] * P[IDX_L2+j]
                for j in RANGE_N: B[IDX_L2+j] += B[IDX_L3+j] * P[IDX_L3+j]
                current_turn += 1
                if current_turn >= T: break
        
        if current_turn >= T: break

        # 購入実行
        if best_action != -1:
            actions.append(f"{best_action//N} {best_action%N}")
            cost = C[best_action] * (P[best_action] + 1)
            current_apples -= cost
            P[best_action] += 1
        else:
            if best_wait_turns == 0:
                actions.append("-1")

        # 1ターン経過(購入したターンの終わり)
        prod = sum(A[j] * B[j] * P[j] for j in RANGE_N)
        current_apples += prod
        for j in RANGE_N: B[j] += B[IDX_L1+j] * P[IDX_L1+j]
        for j in RANGE_N: B[IDX_L1+j] += B[IDX_L2+j] * P[IDX_L2+j]
        for j in RANGE_N: B[IDX_L2+j] += B[IDX_L3+j] * P[IDX_L3+j]
        current_turn += 1
        
    return actions

# ==========================================
# 戦略2: 完全シミュレーション貪欲 (Greedy Simulation)
# 特徴: 毎ターン全通りを最後までシミュレーションし、確実に増える手を選ぶ
# ==========================================
def solve_simulation(N, L, T, K, A, C):
    actions = []
    
    P = [0] * (N * L)
    B = [1] * (N * L)
    
    IDX_L1 = N
    IDX_L2 = N * 2
    IDX_L3 = N * 3
    RANGE_N = range(N)
    
    current_apples = K
    
    for t in range(T):
        remaining_turns = T - 1 - t
        best_score = -1
        best_action = -1
        
        # 1. ベースライン (何もしない)
        sim_apples = current_apples
        sim_B = list(B)
        
        # 高速化のため展開
        for _ in range(remaining_turns + 1):
            prod = 0
            for j in RANGE_N: prod += A[j] * sim_B[j] * P[j]
            sim_apples += prod
            for j in RANGE_N: sim_B[j] += sim_B[IDX_L1+j] * P[IDX_L1+j]
            for j in RANGE_N: sim_B[IDX_L1+j] += sim_B[IDX_L2+j] * P[IDX_L2+j]
            for j in RANGE_N: sim_B[IDX_L2+j] += sim_B[IDX_L3+j] * P[IDX_L3+j]
            
        best_score = sim_apples
        
        # 2. 購入候補探索
        for idx in range(N * L):
            cost = C[idx] * (P[idx] + 1)
            if cost > current_apples: continue
            
            # シミュレーション開始
            s_apples = current_apples - cost
            s_B = list(B)
            
            tgt_l, tgt_j = idx // N, idx % N
            
            for _ in range(remaining_turns + 1):
                prod = 0
                for j in RANGE_N:
                    p_val = P[j] + (1 if tgt_l==0 and j==tgt_j else 0)
                    prod += A[j] * s_B[j] * p_val
                s_apples += prod
                for j in RANGE_N:
                    p_val = P[IDX_L1+j] + (1 if tgt_l==1 and j==tgt_j else 0)
                    s_B[j] += s_B[IDX_L1+j] * p_val
                for j in RANGE_N:
                    p_val = P[IDX_L2+j] + (1 if tgt_l==2 and j==tgt_j else 0)
                    s_B[IDX_L1+j] += s_B[IDX_L2+j] * p_val
                for j in RANGE_N:
                    p_val = P[IDX_L3+j] + (1 if tgt_l==3 and j==tgt_j else 0)
                    s_B[IDX_L2+j] += s_B[IDX_L3+j] * p_val
            
            if s_apples > best_score:
                best_score = s_apples
                best_action = idx
        
        # 行動決定
        if best_action != -1:
            actions.append(f"{best_action//N} {best_action%N}")
            cost = C[best_action] * (P[best_action] + 1)
            current_apples -= cost
            P[best_action] += 1
        else:
            actions.append("-1")
            
        # ターン経過
        prod = 0
        for j in RANGE_N: prod += A[j] * B[j] * P[j]
        current_apples += prod
        for j in RANGE_N: B[j] += B[IDX_L1+j] * P[IDX_L1+j]
        for j in RANGE_N: B[IDX_L1+j] += B[IDX_L2+j] * P[IDX_L2+j]
        for j in RANGE_N: B[IDX_L2+j] += B[IDX_L3+j] * P[IDX_L3+j]
        
    return actions

# ==========================================
# Main
# ==========================================
def solve():
    input = sys.stdin.read
    data = input().split()
    if not data: return
    iterator = iter(data)
    
    N = int(next(iterator))
    L = int(next(iterator))
    T = int(next(iterator))
    K = int(next(iterator))
    
    A = [int(next(iterator)) for _ in range(N)]
    C = [int(next(iterator)) for _ in range(N * L)]
    
    # 2つの戦略を両方実行して比較
    actions1 = solve_heuristic(N, L, T, K, A, C)
    actions2 = solve_simulation(N, L, T, K, A, C)
    
    # スコア評価
    score1 = evaluate(N, L, T, K, A, C, actions1)
    score2 = evaluate(N, L, T, K, A, C, actions2)
    
    # 良い方を採用
    final_actions = actions1 if score1 >= score2 else actions2
    
    # 結果出力
    print("\n".join(final_actions))

if __name__ == "__main__":
    solve()