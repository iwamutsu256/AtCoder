import sys

def solve():
    """
    AHC問題「Apple Incremental Game」に対する貪欲法ソルバー Ver.2。
    
    【戦略概要】
    1. 最優先: ID=0 の Level 1以上の機械。
       - Level 3, 2, 1 の順にチェックし、購入可能なら即座に購入してターン終了。
    2. 次善策: 上記が購入できない場合 (資金稼ぎフェーズ)。
       - 全てのID (j=0...N-1) の Level 0 の機械を候補とする。
       - 「コストパフォーマンス (投資効率)」を計算し、最も効率が良いものを購入する。
       - コスパ = (1ターンあたりの生産増加量) / (強化コスト)
    """

    # --- 入力の読み込み ---
    try:
        # 1行目: N, L, T, K
        line1 = sys.stdin.readline().split()
        if not line1: return
        N, L, T, K = map(int, line1)

        # 2行目: Level 0 の生産能力 A
        A = list(map(int, sys.stdin.readline().split()))

        # 3行目以降: 各Levelの初期コスト C
        C = []
        for _ in range(L):
            C.append(list(map(int, sys.stdin.readline().split())))

    except ValueError:
        return

    # --- 状態変数の初期化 ---
    current_apples = K
    # 機械の個数 B (初期値1)
    B = [[1] * N for _ in range(L)]
    # 機械のパワー P (初期値0)
    P = [[0] * N for _ in range(L)]

    # --- ターンごとの処理 ---
    for t in range(T):
        
        # ---------------------------------------------------------
        # 1. 行動の決定
        # ---------------------------------------------------------
        
        action_i = -1
        action_j = -1
        
        # --- 戦略A: ID=0 の高レベル (Level 1, 2, 3) を優先確保 ---
        # Levelが高い順にチェック
        found_high_level = False
        target_id = 0
        
        for i in range(L - 1, 0, -1): # i = 3, 2, 1
            cost = C[i][target_id] * (P[i][target_id] + 1)
            
            if current_apples >= cost:
                # 買えるなら即決
                action_i = i
                action_j = target_id
                
                # 状態更新
                current_apples -= cost
                P[i][target_id] += 1
                found_high_level = True
                break
        
        # --- 戦略B: 高レベルが買えない場合、Level 0 でコスパ最強を探す ---
        if not found_high_level:
            best_efficiency = -1.0
            best_j = -1
            
            for j in range(N):
                # Level 0 のコスト計算
                cost = C[0][j] * (P[0][j] + 1)
                
                # そもそも所持金で買えないなら候補外
                if current_apples < cost:
                    continue
                
                # コスパ計算
                # 強化による生産増加量 = A[j] * (現在の個数)
                # ※ 強化すると P が +1 され、生産式 A * B * P が A * B * (P+1) になるため、
                #    差分は A * B となる。
                gain = A[j] * B[0][j]
                
                # 効率 = 増加量 / コスト
                efficiency = gain / cost
                
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_j = j
            
            # 最も効率が良いものが買えるなら購入
            if best_j != -1:
                action_i = 0
                action_j = best_j
                
                # 状態更新
                cost = C[0][best_j] * (P[0][best_j] + 1)
                current_apples -= cost
                P[0][best_j] += 1

        # 行動の出力
        if action_i != -1:
            print(f"{action_i} {action_j}")
        else:
            print("-1")

        # ---------------------------------------------------------
        # 2. 生産のシミュレーション (次のターンのために状態更新)
        # ---------------------------------------------------------
        for i in range(L):
            for j in range(N):
                count = B[i][j]
                power = P[i][j]

                if i == 0:
                    # Level 0: りんごを生産
                    production = A[j] * count * power
                    current_apples += production
                else:
                    # Level >= 1: 1つ下のLevelの機械を生産
                    # Level i の機械が、Level i-1 の機械を生み出す
                    new_machines = count * power
                    B[i-1][j] += new_machines

if __name__ == "__main__":
    solve()