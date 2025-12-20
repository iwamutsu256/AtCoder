import sys
import time
import math
import random
from typing import List, Tuple

# --- 定数設定 ---
TIME_LIMIT = 1.85
LOG_INTERVAL = 5000  # 高速化されたのでログ出力頻度を上げる

class ProblemData:
    def __init__(self):
        try:
            line1 = sys.stdin.readline().split()
            if not line1:
                self.N, self.L, self.T, self.K = 10, 4, 500, 1
                self.A = [1] * 10
                self.C = [[10] * 10 for _ in range(4)]
                return
            self.N, self.L, self.T, self.K = map(int, line1)
            self.A = list(map(int, sys.stdin.readline().split()))
            self.C = []
            for _ in range(self.L):
                self.C.append(list(map(int, sys.stdin.readline().split())))
        except ValueError:
            sys.exit(0)

DATA = ProblemData()

# --- 数式計算用のヘルパー関数 (O(1)) ---
# S_k(n) = sum_{x=0}^{n-1} x^k
# 0からn-1までの和であることに注意（nターン経過時の増分計算用）

def S0(n): # sum 1
    return n

def S1(n): # sum x
    return n * (n - 1) // 2

def S2(n): # sum x^2
    return n * (n - 1) * (2 * n - 1) // 6

def S3(n): # sum x^3
    val = n * (n - 1) // 2
    return val * val

class FastEvaluator:
    """数式ジャンプを用いた超高速評価クラス"""

    @staticmethod
    def evaluate(ops: List[Tuple[int, int]]) -> float:
        """
        操作リスト ops (順序のみ) を受け取り、
        可能な限り最速で購入していった場合の最終りんご数を返す。
        """
        # --- 初期状態 ---
        # 頻繁にアクセスするデータはローカル変数に展開
        T_limit = DATA.T
        N = DATA.N
        L = DATA.L
        DataA = DATA.A
        DataC = DATA.C
        
        # 動的な状態
        current_apples = float(DATA.K) # log計算用にfloatで保持
        current_turn = 0
        
        # B[i][j]: Level i, ID j の個数
        # P[i][j]: Level i, ID j のパワー
        # 高速化のため、1次元配列または単純なリスト管理でも良いが
        # 計算式が複雑になるので可読性維持のため2次元配列を使う
        B = [[1] * N for _ in range(L)]
        P = [[0] * N for _ in range(L)]
        
        # --- 操作ループ ---
        for lvl, mid in ops:
            if current_turn >= T_limit:
                break
                
            # 次の目標コスト
            # cost = C * (P + 1)
            target_cost = DataC[lvl][mid] * (P[lvl][mid] + 1)
            
            # 足りない資金
            needed = target_cost - current_apples
            
            if needed <= 0:
                # すぐ買えるならターン消費なしで購入（同ターン内での複数購入）
                # ただし問題のルール上「1ターンに1回行動」なので、
                # 厳密には「資金があっても1ターン消費」が必要。
                # ここでは「資金が貯まるまでの待機ターン」＋「購入アクション(1ターン)」と考える。
                wait_turns = 0
            else:
                # 資金が足りない場合、何ターン生産すれば貯まるか計算
                wait_turns = FastEvaluator._find_wait_turns(needed, B, P, T_limit - current_turn, DataA)
                
                # 買えないまま時間切れの場合
                if wait_turns is None:
                    # 残り時間を全て生産に費やして終了
                    remaining = T_limit - current_turn
                    current_apples += FastEvaluator._calc_gained_apples(remaining, B, P, DataA)
                    current_turn = T_limit
                    break

            # 待機期間の生産成果を加算
            # 待機ターン数が0でも計算は走るが結果は0なのでOK
            if wait_turns > 0:
                # りんごの加算
                gained_apples = FastEvaluator._calc_gained_apples(wait_turns, B, P, DataA)
                current_apples += gained_apples
                
                # 機械の個数(B)の更新
                FastEvaluator._update_machines(wait_turns, B, P)
                
                current_turn += wait_turns

            # 購入アクション (1ターン消費)
            # 1ターン分の生産を行ってから、購入コストを支払い、能力を上げる
            if current_turn < T_limit:
                # 1. 生産 (このターンの生産)
                current_apples += FastEvaluator._calc_gained_apples(1, B, P, DataA)
                FastEvaluator._update_machines(1, B, P)
                current_turn += 1
                
                # 2. 購入 (強化)
                # ここで資金チェック（数式予測でギリギリ届かない誤差のケア）
                if current_apples >= target_cost:
                    current_apples -= target_cost
                    P[lvl][mid] += 1
                else:
                    # 万が一足りない場合（計算誤差など）、さらに1ターン待つなどの処理が必要だが
                    # 整数計算ならズレないはず。念のためスキップ扱いにしないよう注意。
                    # ここでは簡単のため「買えなかったことにして進む」(=ペナルティ)とするが、
                    # 本来はループで再待機すべき。
                    pass
        
        # --- 残り時間の消化 (変更: ID=0 Level 0 を貪欲に買い続ける) ---
        # リストが尽きても時間がある場合、何もしないのは損なので
        # 最も安価な ID=0, Level 0 を買えるだけ買う処理を追加
        target_lvl = 0
        target_id = 0
        
        while current_turn < T_limit:
            target_cost = DataC[target_lvl][target_id] * (P[target_lvl][target_id] + 1)
            needed = target_cost - current_apples
            
            wait_turns = 0
            if needed > 0:
                wait_turns = FastEvaluator._find_wait_turns(needed, B, P, T_limit - current_turn, DataA)
                if wait_turns is None:
                    # もう買えないので残り時間を生産に充てて終了
                    remaining = T_limit - current_turn
                    current_apples += FastEvaluator._calc_gained_apples(remaining, B, P, DataA)
                    current_turn = T_limit
                    break
            
            # 待機
            if wait_turns > 0:
                current_apples += FastEvaluator._calc_gained_apples(wait_turns, B, P, DataA)
                FastEvaluator._update_machines(wait_turns, B, P)
                current_turn += wait_turns
                
            # 購入 (1ターン消費)
            if current_turn < T_limit:
                # 生産
                current_apples += FastEvaluator._calc_gained_apples(1, B, P, DataA)
                FastEvaluator._update_machines(1, B, P)
                current_turn += 1
                
                # 購入実行
                if current_apples >= target_cost:
                    current_apples -= target_cost
                    P[target_lvl][target_id] += 1
            
        # 修正: log2 を取って返す
        if current_apples <= 0:
            return 0.0
        return math.log2(float(current_apples))

    @staticmethod
    def _calc_gained_apples(t: int, B: List[List[int]], P: List[List[int]], A: List[int]) -> int:
        """
        現在の B, P の状態で t ターン経過したときの「りんご増加量」を
        O(1) の数式で計算する。
        """
        if t <= 0: return 0
        
        total_gained = 0
        N = len(A)
        
        # 係数の事前計算 (ループ外に出せばさらに速いが、N=10なのでここで計算)
        # S0(t), S1(t), S2(t), S3(t) を使う
        s0 = S0(t)
        s1 = S1(t)
        s2 = S2(t)
        s3 = S3(t)
        
        for j in range(N):
            # Level 0 のパワーがないと何も生産されない
            p0 = P[0][j]
            if p0 == 0: continue
            
            # 各項の係数計算
            # 1. B0 の寄与 (定数項): B0 * P0 * A
            term0 = B[0][j]
            
            # 2. B1 の寄与 (1次の項): B1 * P1 * P0 * A
            p1 = P[1][j]
            term1 = 0
            term2 = 0
            term3 = 0
            
            if p1 > 0:
                term1 = B[1][j] * p1
                
                # 3. B2 の寄与 (2次の項)
                p2 = P[2][j]
                if p2 > 0:
                    term2 = B[2][j] * p2 * p1
                    
                    # 4. B3 の寄与 (3次の項)
                    p3 = P[3][j]
                    if p3 > 0:
                        term3 = B[3][j] * p3 * p2 * p1
            
            # 総和: A[j] * P0 * (term0*S0 + term1*S1 + term2*S2 + term3*S3)
            # ※ term2, term3 は B3, B2 からの波及分
            
            # 正確な多項式の適用
            # Level 1 から Level 0 への流入: B1(tau) = B1 + B2*P2*tau + B3*P3*P2*tau^2/2...
            # この展開は複雑なので、上の階層から順に係数を確定させる
            
            # 係数C0, C1, C2, C3 を求める
            # B0(tau) = c0 + c1*tau + c2*tau*(tau-1)/2 + ...
            # 離散和の公式に当てはめるため、増分ベースで考える
            
            # 簡単化: 
            # contribution = sum_{tau=0}^{t-1} A[j] * P0 * B0(tau)
            
            # B0(tau) の成分分解:
            # 1. 初期B0由来: B[0][j] (定数) -> 和は B[0][j] * t
            val = B[0][j] * s0
            
            if p1 > 0:
                # 2. 初期B1由来: B[1][j] が毎ターン B0 を B[1][j]*P1 増やす
                # B0への寄与は 等差数列の和 -> B[1][j]*P1 * S1(t)
                val += B[1][j] * p1 * s1
                
                if p2 > 0:
                    # 3. 初期B2由来: B[2][j] -> B1増 -> B0増
                    # 2段階の和 -> B[2][j]*P2*P1 * S2(t)
                    val += B[2][j] * p2 * p1 * s2
                    
                    if p3 > 0:
                        # 4. 初期B3由来: B[3][j] -> B2増 -> B1増 -> B0増
                        # 3段階の和 -> B[3][j]*P3*P2*P1 * S3(t)
                        val += B[3][j] * p3 * p2 * p1 * s3
            
            total_gained += A[j] * p0 * val
            
        return total_gained

    @staticmethod
    def _update_machines(t: int, B: List[List[int]], P: List[List[int]]):
        """
        t ターン経過後の B (機械の数) を O(1) で更新する
        """
        if t <= 0: return
        
        N = len(B[0])
        s0 = S0(t)
        s1 = S1(t)
        s2 = S2(t)
        
        for j in range(N):
            # 上のレベルから順不同だが、依存関係に注意して計算
            # B3 は不変
            
            # B2 の更新: B2 += B3 * P3 * t
            p3 = P[3][j]
            b3 = B[3][j]
            # B2への増分を計算するために一時保存が必要か？
            # いや、B2の更新にB2の初期値は不要、B3初期値を使う。
            # ただしB1の更新にはB2の初期値が必要。
            # なので古い値を保持しておくか、計算順序を工夫する。
            
            # 下位レベルへの影響係数
            p2 = P[2][j]
            p1 = P[1][j]
            
            # --- B0 の更新 ---
            # B0 += B1*P1*S0 + B2*P2*P1*S1 + B3*P3*P2*P1*S2
            # ここでの B1, B2, B3 は「期間開始時の値」
            if p1 > 0:
                term1 = B[1][j] * p1 * s0
                term2 = 0
                term3 = 0
                if p2 > 0:
                    term2 = B[2][j] * p2 * p1 * s1
                    if p3 > 0:
                        term3 = B[3][j] * p3 * p2 * p1 * s2
                B[0][j] += term1 + term2 + term3
            
            # --- B1 の更新 ---
            # B1 += B2*P2*S0 + B3*P3*P2*S1
            if p2 > 0:
                term1 = B[2][j] * p2 * s0
                term2 = 0
                if p3 > 0:
                    term2 = B[3][j] * p3 * p2 * s1
                B[1][j] += term1 + term2
            
            # --- B2 の更新 ---
            # B2 += B3*P3*S0 (つまり B3*P3*t)
            if p3 > 0:
                B[2][j] += B[3][j] * p3 * s0

    @staticmethod
    def _find_wait_turns(needed: int, B, P, max_turns: int, A) -> int:
        """
        needed 以上のりんごを稼ぐのに必要な最小ターン数を二分探索で求める。
        """
        # 単調増加関数なので二分探索が可能
        low = 1
        high = max_turns
        ans = None
        
        while low <= high:
            mid = (low + high) // 2
            gained = FastEvaluator._calc_gained_apples(mid, B, P, A)
            
            if gained >= needed:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        return ans

# --- 焼きなましソルバー本体 ---

def solve():
    start_time = time.time()
    
    # 1. 初期解生成 (貪欲法ベース)
    # 既存の貪欲法ロジックを流用してリストを作成
    initial_ops = []
    
    # 簡易貪欲シミュレーションを行ってリストを作る
    # (ここではSolverの整合性を保つため、シンプルなヒューリスティックでリストを作る)
    # 戦略: ID=0 の Level 1,2,3 を買える順に買う
    for _ in range(50): # 適当な長さ
        lvl = random.randint(0, 3)
        initial_ops.append((lvl, 0)) # ID=0のみに絞ってみる（むつきさんの戦略）

    # 最初の解が空だと困るので、最低限のリストを持たせる
    # 実際にはもっと賢い初期化が良いが、SAで最適化させる
    
    current_ops = initial_ops[:]
    current_score = FastEvaluator.evaluate(current_ops)
    
    best_ops = current_ops[:]
    best_score = current_score
    
    sys.stderr.write(f"# Init Score: {best_score:.4f}\n")
    
    # --- SA ---
    # 修正: logスコアに合わせて温度を調整
    # スコアは概ね 0 ~ 100 程度の範囲になる
    T0 = 2.0   # 初期温度
    T1 = 0.05  # 終端温度
    loop_count = 0
    
    while True:
        loop_count += 1
        if loop_count % LOG_INTERVAL == 0:
            now = time.time()
            if now - start_time > TIME_LIMIT:
                break
            sys.stderr.write(f"# Loop: {loop_count}, Best: {best_score:.4f}\n")
            
            progress = (now - start_time) / TIME_LIMIT
            temperature = T0 + (T1 - T0) * progress # 線形冷却
        
        # 近傍操作
        neighbor_ops = current_ops[:]
        mode = random.random()
        L_ops = len(neighbor_ops)
        
        if mode < 0.4: # Add
            pos = random.randint(0, L_ops)
            # 制約: ID=0 のみ (あるいは緩和して良いならランダム)
            # ここでは「ID0のLevel1購入以降はID0のみ」という制約を守るように生成
            # 簡易的に常にID=0を追加する戦略にする（ID0特化）
            new_val = (random.randint(0, DATA.L - 1), 0)
            neighbor_ops.insert(pos, new_val)
            
        elif mode < 0.7: # Delete
            if L_ops > 0:
                pos = random.randint(0, L_ops - 1)
                neighbor_ops.pop(pos)
                
        elif mode < 0.9: # Change
            if L_ops > 0:
                pos = random.randint(0, L_ops - 1)
                neighbor_ops[pos] = (random.randint(0, DATA.L - 1), 0)
                
        else: # Swap
            if L_ops >= 2:
                p1 = random.randint(0, L_ops - 1)
                p2 = random.randint(0, L_ops - 1)
                neighbor_ops[p1], neighbor_ops[p2] = neighbor_ops[p2], neighbor_ops[p1]
        
        # 評価
        new_score = FastEvaluator.evaluate(neighbor_ops)
        delta = new_score - current_score
        
        if delta > 0:
            current_ops = neighbor_ops
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_ops = neighbor_ops[:]
        else:
            try:
                # 温度管理は適宜調整
                if random.random() < math.exp(delta / temperature):
                    current_ops = neighbor_ops
                    current_score = new_score
            except:
                pass

    # --- 最終出力 ---
    output_schedule(best_ops)

def output_schedule(ops: List[Tuple[int, int]]):
    """
    最終的な出力生成（ここも数式ジャンプと同じロジックで再計算して出力）
    """
    # 出力用に1ターンずつ回す（出力形式に合わせるため）
    # ただし、ロジックはFastEvaluatorと一致させる必要がある
    # ここでは簡易的に「買えるかチェック」を行う標準シミュレーションを使用
    
    # 完全に再現するためには、FastEvaluatorのロジックで「何ターン待機」かを計算し、
    # その分だけ "-1" を出力し、購入ターンに "lvl mid" を出力する。
    
    B = [[1] * DATA.N for _ in range(DATA.L)]
    P = [[0] * DATA.N for _ in range(DATA.L)]
    current_apples = DATA.K
    current_turn = 0
    ops_idx = 0
    
    while current_turn < DATA.T:
        did_buy = False
        
        # 次に買うターゲットの決定
        # リストが残っていればそれを使う、なければ ID=0, Level 0
        if ops_idx < len(ops):
            lvl, mid = ops[ops_idx]
        else:
            lvl, mid = 0, 0
            
        target_cost = DATA.C[lvl][mid] * (P[lvl][mid] + 1)
        
        if current_apples >= target_cost:
            # 購入実行
            print(f"{lvl} {mid}")
            current_apples -= target_cost
            P[lvl][mid] += 1
            if ops_idx < len(ops):
                ops_idx += 1
            did_buy = True
        
        if not did_buy:
            print("-1")
            
        # 生産処理 (1ターン分)
        # Bの更新用の一時変数
        next_B = [row[:] for row in B]
        
        # Level 0 生産
        prod = 0
        for j in range(DATA.N):
            if P[0][j] > 0:
                prod += DATA.A[j] * B[0][j] * P[0][j]
        current_apples += prod
        
        # Level 1以上 生産
        for i in range(1, DATA.L):
            for j in range(DATA.N):
                if P[i][j] > 0:
                    next_B[i-1][j] += B[i][j] * P[i][j]
        B = next_B
        current_turn += 1

if __name__ == "__main__":
    solve()