import sys

def solve():
    """
    AHC問題「Apple Incremental Game」に対する貪欲法ソルバー。
    
    【戦略概要】
    - 操作対象を ID=0 の機械のみに限定する。
    - 毎ターン、所持しているりんごで購入可能な「最もLevelが高い機械」を強化する。
    - 購入できない場合は何もしない。
    """

    # --- 入力の読み込み ---
    try:
        # 1行目: N, L, T, K
        line1 = sys.stdin.readline().split()
        if not line1: return # 入力がない場合は終了
        N, L, T, K = map(int, line1)

        # 2行目: Level 0 の生産能力 A
        A = list(map(int, sys.stdin.readline().split()))

        # 3行目以降: 各Levelの初期コスト C
        # C[i][j] が Level i, ID j のコスト
        C = []
        for _ in range(L):
            C.append(list(map(int, sys.stdin.readline().split())))

    except ValueError:
        # 万が一入力形式が崩れていた場合のエラーハンドリング
        return

    # --- 状態変数の初期化 ---
    
    # 現在のりんごの数
    current_apples = K

    # 機械の個数 B[i][j] (初期値はすべて1)
    # 問題文: "計画開始時点ではすべて 1 である"
    B = [[1] * N for _ in range(L)]

    # 機械のパワー P[i][j] (初期値はすべて0)
    # 問題文: "開始時点ではすべて 0 である"
    P = [[0] * N for _ in range(L)]

    # --- ターンごとの処理 ---
    for t in range(T):
        
        # ---------------------------------------------------------
        # 1. 行動の決定 (貪欲法)
        # ---------------------------------------------------------
        
        target_id = 0  # 今回はID 0のみを対象とする
        action_i = -1  # 強化するLevel (-1は何もしない)
        action_j = -1  # 強化するID

        # --- 貪欲法: 核心部 ---
        # Levelが高い順 (L-1 から 0) に、強化可能かチェックする
        for i in range(L - 1, -1, -1):
            
            # 現在のパワー P[i][0] を取得
            current_p = P[i][target_id]
            
            # 強化に必要なコスト計算: C[i][j] * (P[i][j] + 1)
            cost = C[i][target_id] * (current_p + 1)
            
            # コストが払えるなら強化を決定
            if current_apples >= cost:
                action_i = i
                action_j = target_id
                
                # りんごを消費
                current_apples -= cost
                
                # パワーを更新 (出力用ではなく内部状態用)
                P[i][target_id] += 1
                
                # 今回の戦略では、1つ強化したらそのターンの行動は終了
                break

        # 行動の出力
        if action_i != -1:
            print(f"{action_i} {action_j}")
        else:
            print("-1")

        # ---------------------------------------------------------
        # 2. 生産のシミュレーション (次のターンのために状態更新)
        # ---------------------------------------------------------
        # 問題文: "Level 0, 1, 2, 3 の順に、すべての機械 ji について以下の処理を行う"
        
        for i in range(L):
            for j in range(N):
                # 現在の個数とパワー
                count = B[i][j]
                power = P[i][j]

                if i == 0:
                    # Level 0: りんごを生産
                    # 生産量 = A[j] * B[0][j] * P[0][j]
                    production = A[j] * count * power
                    current_apples += production
                else:
                    # Level >= 1: 1つ下のLevelの機械を生産
                    # 増加数 = B[i][j] * P[i][j]
                    # 生産されるのは Level i-1 の機械
                    new_machines = count * power
                    B[i-1][j] += new_machines

    # 最終的なスコアなどは、ここでは計算不要 (出力は行動のみ)

if __name__ == "__main__":
    solve()