import sys
import heapq

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
    
    C = [int(next(iterator)) for _ in range(N * L)]
    
    # --- 2. 数列の和の事前計算 ---
    # シミュレーションループをO(1)にするための累積和テーブル
    # S1[t] = sum(k for k in 0..t-1) = t*(t-1)/2
    # S_S1[t] = sum(S1[k] for k in 0..t-1)
    # S_S1_comb[t] = sum( (S2[k] - S1[k])/2 for k in 0..t-1 ) where S2 is sum of squares
    
    S1 = [0] * (T + 1)
    S_S1 = [0] * (T + 1)
    S_S1_comb = [0] * (T + 1)
    
    for t in range(1, T + 1):
        k = t - 1
        val_s1 = k * (k + 1) // 2
        S1[t] = S1[t-1] + k # Wait, sum is 0 to t-1. k is the term index.
        # Strict formula: sum_{i=0}^{t-1} i = t*(t-1)/2. 
        # Let's use direct formula for arbitrary t access
        pass

    # 公式で直接計算する関数（配列アクセスより計算の方が速い場合もあるが、テーブル化する）
    # テーブル再構築
    # Tが小さいのでループで作る
    
    # 0 to t-1 の和
    memo_S1 = [0] * (T + 2)
    memo_S_S1 = [0] * (T + 2)
    memo_S_comb = [0] * (T + 2)
    
    current_S1 = 0
    current_S_S1 = 0
    current_S_comb = 0
    
    for t in range(1, T + 1):
        # 項 k = t-1
        k = t - 1
        
        # S1(k) = 0 + 1 + ... + k
        # ここでの定義:
        # Level 2 produces B1 with rate B2*P2.
        # B1(t) = B1_0 + sum_{m=0}^{t-1} (B2_0 + B3_0*P3*m)*P2
        #       = B1_0 + B2_0*P2*t + B3_0*P3*P2 * (sum_{m=0}^{t-1} m)
        # term sum_m is n*(n-1)/2 for n=t.
        
        # We need cumulative sums of these terms for higher levels.
        # Let's precompute exactly what's needed.
        
        term_k = k
        term_s1 = k * (k - 1) // 2
        term_s2 = k * (k - 1) * (2 * k - 1) // 6
        term_comb = (term_s2 - term_s1) // 2
        
        # 累積和テーブルへの格納 (index t は「残りターン t」に対応させる)
        # しかしループ内では 0..t-1 の総和が必要
        pass

    # --- 公式定義 ---
    # sum_i(t) = sum_{k=0}^{t-1} k = t*(t-1)//2
    def get_sum_i(t):
        return t * (t - 1) // 2

    # sum_s1(t) = sum_{k=0}^{t-1} k*(k-1)//2
    #           = 1/2 * ( sum k^2 - sum k )
    # sum k^2 = (t-1)*t*(2t-2+1)//6 = t*(t-1)*(2t-1)//6
    # sum k   = t*(t-1)//2
    def get_sum_s1(t):
        if t <= 0: return 0
        n = t
        sum_sq = n * (n - 1) * (2 * n - 1) // 6
        sum_lin = n * (n - 1) // 2
        return (sum_sq - sum_lin) // 2

    # sum_comb(t) = sum_{k=0}^{t-1} ( sum_{m=0}^{k-1} m(m-1)/2 )
    # This is getting complex. Precomputing is safer.
    
    TABLE_SUM_I = [0] * (T + 1)
    TABLE_SUM_S1 = [0] * (T + 1)
    TABLE_SUM_COMB = [0] * (T + 1)
    
    for t in range(1, T + 1):
        k = t - 1 # term index
        
        # For Level 2 contribution to B1: k
        # Sum over 0..t-1 is t*(t-1)/2
        TABLE_SUM_I[t] = k * (k + 1) // 2
        
        # For Level 3 contribution to B1: k*(k-1)/2 (This is sum_i(k))
        # We need sum over 0..t-1 of sum_i(k)
        # This is TABLE_SUM_S1
        val_s1 = k * (k - 1) // 2 if k > 0 else 0
        TABLE_SUM_S1[t] = TABLE_SUM_S1[t-1] + val_s1

        # For Level 3 contribution to B0:
        # It involves the cumulative sum of the previous term.
        # Let's stick to the coefficients logic.
        # Coeff for B3->Apples involves triple summation.
        # Let's precompute the multipliers for B0, B1, B2, B3 contribution to Apples.
        
    # --- 係数テーブル (Multiplier) ---
    # RemT (残りターン) に対する、各レベルの機械1台(Power=1)あたりの総生産りんご数への寄与係数
    # これがあれば、prediction = sum(B[i][j] * P[i][j] * Mult[i][RemT]) で求まる！
    
    Mult_L0 = [0] * (T + 1) # B0 * P0 -> Apples
    Mult_L1 = [0] * (T + 1) # B1 * P1 -> B0 -> Apples
    Mult_L2 = [0] * (T + 1) # B2 * P2 -> B1 -> B0 -> Apples
    Mult_L3 = [0] * (T + 1) # B3 * P3 -> B2 -> B1 -> B0 -> Apples
    
    # Simulation to compute exact multipliers
    # 仮に B=[1,0,0,0], P=[1,0,0,0] でスタートしたときのTターン後の増分
    
    for rem_t in range(1, T + 1):
        # 1. Level 0 contribution
        # Every turn produce 1 apple. Total rem_t.
        Mult_L0[rem_t] = rem_t
        
        # 2. Level 1 contribution
        # t=0: B1 produces 1 B0.
        # t=1: That B0 produces 1 Apple.
        # ...
        # Total apples is sum_{k=0}^{rem_t-1} k = rem_t*(rem_t-1)/2
        Mult_L1[rem_t] = rem_t * (rem_t - 1) // 2
        
        # 3. Level 2 contribution
        # Produces B1. B1 produces B0.
        # Coeff is sum of Mult_L1[k] for k in 0..rem_t-1 ?
        # Not exactly.
        # Let's run a tiny DP to fill these tables perfectly.
        pass

    # DP for multipliers
    # m[lvl][t]
    m = [[0] * (T + 1) for _ in range(4)]
    
    for t in range(1, T + 1):
        # L0 contribution: Adds 1 apple per turn
        m[0][t] = m[0][t-1] + 1
        
        # L1 contribution: Adds 1 L0 per turn.
        # The added L0 will work for (t-1) turns ? No.
        # Problem: L0 prod, THEN L1 prod.
        # So L1 produces B0 at end of turn. That B0 starts working next turn.
        # So it contributes m[0][t-1]
        m[1][t] = m[1][t-1] + m[0][t-1]
        
        # L2 contribution: Adds 1 L1. Contributes m[1][t-1]
        m[2][t] = m[2][t-1] + m[1][t-1]
        
        # L3 contribution
        m[3][t] = m[3][t-1] + m[2][t-1]
        
    Mult_L0 = m[0]
    Mult_L1 = m[1]
    Mult_L2 = m[2]
    Mult_L3 = m[3]
    
    # ----------------------------------------------------
    
    # 状態: (apples, B_tuple, P_tuple)
    # 高速化のため、BとPはタプルで持つ
    init_B = tuple([1] * (N * L))
    init_P = tuple([0] * (N * L))
    
    # ビーム設定
    # 0.6秒で終わるならかなり広げられる。
    BEAM_WIDTH = 200
    
    # beam: list of (score, apples, B, P)
    # score is predicted total apples
    beam = [(0, K, init_B, init_P)]
    
    # 履歴復元用
    # history[t] = { (B, P): (prev_B, prev_P, act_i, act_j) }
    history = [{} for _ in range(T)]
    
    IDX_L0 = 0
    IDX_L1 = N
    IDX_L2 = 2 * N
    IDX_L3 = 3 * N
    
    RANGE_ALL = range(N * L)
    
    for t in range(T):
        rem_t = T - 1 - t
        next_beam_candidates = [] # heap
        
        # Multipliers for this remaining time
        # これを使うと、現在の (B, P) が将来生み出すりんご数が O(1) で出る
        # Base Production = sum( A[j] * B[i][j] * P[i][j] * Mult[i][rem_t] )
        
        w0 = Mult_L0[rem_t]
        w1 = Mult_L1[rem_t]
        w2 = Mult_L2[rem_t]
        w3 = Mult_L3[rem_t]
        
        # 重複チェック用
        seen_states = {}
        
        for _, curr_apples, curr_B, curr_P in beam:
            
            # 1. Base potential (今の能力で放置した場合の将来の生産量)
            # 差分計算のために、まずベースを計算しておく
            # (ここが一番重いので、前のターンからの差分更新ができればベストだが、
            #  Bが変わるので毎回計算必要。しかしループなしなので速い)
            
            # 高速化: N*L ループ
            # A[j] * B * P * W
            # Pythonのループは遅いので、展開したいが40回ならOK
            
            base_potential = 0
            for j in range(N):
                # Level 0
                idx = j
                if curr_P[idx] > 0:
                    base_potential += A[j] * curr_B[idx] * curr_P[idx] * w0
                # Level 1
                idx = IDX_L1 + j
                if curr_P[idx] > 0:
                    base_potential += A[j] * curr_B[idx] * curr_P[idx] * w1
                # Level 2
                idx = IDX_L2 + j
                if curr_P[idx] > 0:
                    base_potential += A[j] * curr_B[idx] * curr_P[idx] * w2
                # Level 3
                idx = IDX_L3 + j
                if curr_P[idx] > 0:
                    base_potential += A[j] * curr_B[idx] * curr_P[idx] * w3
            
            # --- アクション生成 ---
            # 候補: -1 と、買えるもの全て
            # 買えるものチェック
            
            # 1. 何もしない
            # この場合、Pは変わらない。Bだけが進む。
            # 「次のターンのスコア」を予測する必要がある。
            # 次のターンになると rem_t が 1 減る。
            # しかし beam の比較基準は「最終的なリンゴ数」なので、
            # 「今のターンに行動した後、残りターン放置」で統一して比較すればよい。
            
            # Action: None
            # Score = current_apples + base_potential
            # 次の状態の B は更新されるが、score計算上は「この瞬間の潜在能力」で測るのが
            # 0.6秒コード(全シミュレーション)と等価。
            # 正確には「行動後の生産」を加算し、Bを更新した状態をキューに入れる。
            
            # 生産処理 (共通)
            prod_apples = 0
            for j in range(N):
                prod_apples += A[j] * curr_B[j] * curr_P[j]
            
            # 次のB
            next_B_noact = list(curr_B)
            for j in range(N):
                next_B_noact[j] += curr_B[IDX_L1+j] * curr_P[IDX_L1+j]
                next_B_noact[IDX_L1+j] += curr_B[IDX_L2+j] * curr_P[IDX_L2+j]
                next_B_noact[IDX_L2+j] += curr_B[IDX_L3+j] * curr_P[IDX_L3+j]
            next_B_noact_t = tuple(next_B_noact)
            
            # 何もしない場合のスコア = (現在の所持金 + 生産分) + (更新後B, P での将来生産)
            # しかし base_potential は「今の B, P」での将来生産。
            # 正しい評価関数:
            # Score = (curr_apples + prod_apples) + Future(next_B, curr_P, rem_t-1)
            # これは重い。
            # 単純化: Score = curr_apples + base_potential (今のB,Pがrem_t間で生む量)
            # これは「今ターン終了時の生産」も含んでいるので正確。
            
            score_noact = curr_apples + base_potential
            
            # Heapに追加 (-score, apples, B, P, act_i, act_j, prev_B, prev_P)
            heapq.heappush(next_beam_candidates, (-score_noact, curr_apples + prod_apples, next_B_noact_t, curr_P, -1, -1, curr_B, curr_P))
            
            # 2. 強化する
            for idx in RANGE_ALL:
                p_val = curr_P[idx]
                cost = C[idx] * (p_val + 1)
                
                if cost <= curr_apples:
                    # 強化実行
                    rem_apples = curr_apples - cost
                    
                    # 差分計算: Pが1増えたことによる将来生産の増加分
                    # Delta = A[j] * B[idx] * 1 * Weight
                    # ※Bは現在のものを使う
                    
                    lvl = idx // N
                    j = idx % N
                    
                    weight = 0
                    if lvl == 0: weight = w0
                    elif lvl == 1: weight = w1
                    elif lvl == 2: weight = w2
                    elif lvl == 3: weight = w3
                    
                    delta_score = A[j] * curr_B[idx] * weight
                    new_score = rem_apples + base_potential + delta_score
                    
                    # 次の状態作成
                    # P更新
                    # tupleの1要素だけ変えるのは面倒だがやるしかない
                    # next_P = list(curr_P); next_P[idx] += 1; tuple... 遅いか？
                    # Pは各候補で変わる。Bは共通(生産ロジックはP依存だが、このターンの生産は元のP依存)
                    # 問題文: "強化する... Pi,jを1増やす" -> "Level 0... 処理を行う"
                    # つまり強化は生産の前！
                    # よって、このターンの生産量も増える！
                    
                    # 修正:
                    # 強化 -> P増える -> 生産 (増えたPで計算) -> B増える
                    
                    # 正しい Delta 計算:
                    # 1. コスト支払い (-cost)
                    # 2. 将来生産の増加 (+ A[j] * B * 1 * Weight)
                    # これでOK。Weightは「このターン含む残り全ターンの生産」をカバーしているはず。
                    # w0[t] = t. つまりこのターン(1) + 残り(t-1) = t. OK.
                    
                    # 次のBの計算
                    # 強化されたPで生産が行われるので、next_B も変わる可能性がある
                    # next_B_act は next_B_noact と異なる
                    
                    # 差分更新でBを作る
                    # もし強化したのが L1, L2, L3 なら、その下のレベルのBが増える
                    # L0強化ならBは変わらない(Applesが増えるだけだがそれはScoreに含まれる)
                    
                    next_B_act = list(next_B_noact) # ベースをコピー
                    # 追加生産分
                    if lvl > 0:
                        target_b_idx = (lvl - 1) * N + j
                        # 増分: curr_B[idx] * 1
                        next_B_act[target_b_idx] += curr_B[idx]
                    
                    next_B_act_t = tuple(next_B_act)
                    
                    # P更新
                    # ここは毎回生成必要
                    next_P_list = list(curr_P)
                    next_P_list[idx] += 1
                    next_P_t = tuple(next_P_list)
                    
                    # 残金更新 (このターンの生産分を加算)
                    # ベース生産 + 強化による追加生産
                    prod_increase = 0
                    if lvl == 0:
                        prod_increase = A[j] * curr_B[idx] # * 1
                    
                    final_apples = rem_apples + prod_apples + prod_increase
                    
                    heapq.heappush(next_beam_candidates, (-new_score, final_apples, next_B_act_t, next_P_t, idx // N, idx % N, curr_B, curr_P))

        # --- ビーム選抜 ---
        new_beam = []
        count = 0
        
        while next_beam_candidates and count < BEAM_WIDTH:
            neg_s, app, nb, np, ai, aj, pb, pp = heapq.heappop(next_beam_candidates)
            
            # 重複チェック
            if (nb, np) in seen_states:
                if seen_states[(nb, np)] >= -neg_s: # スコア比較
                    continue
            seen_states[(nb, np)] = -neg_s
            
            new_beam.append((-neg_s, app, nb, np))
            history[t][(nb, np)] = (pb, pp, ai, aj)
            count += 1
            
        beam = new_beam
        
        # 詰み防止
        if not beam: break

    # --- 結果復元 ---
    beam.sort(key=lambda x: x[0], reverse=True) # score降順
    best_res = beam[0]
    curr_B, curr_P = best_res[2], best_res[3]
    
    ans = []
    for t in range(T-1, -1, -1):
        if (curr_B, curr_P) not in history[t]:
            ans.append((-1, -1)) # Error fallback
            break
        pb, pp, ai, aj = history[t][(curr_B, curr_P)]
        ans.append((ai, aj))
        curr_B, curr_P = pb, pp
        
    ans.reverse()
    for ai, aj in ans:
        if ai == -1:
            print("-1")
        else:
            print(f"{ai} {aj}")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()