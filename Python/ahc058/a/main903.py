import sys
import time
import math
import random
from typing import List, Tuple

# --- 定数設定 ---
TIME_LIMIT = 1.85  # 実行制限時間
LOG_INTERVAL = 2000  # 何回ループするごとにログを出すか

class ProblemData:
    """入力データを管理するクラス"""
    def __init__(self):
        try:
            # 1行目: N, L, T, K
            line1 = sys.stdin.readline().split()
            if not line1:
                # ローカルテスト用のダミーデータ
                self.N, self.L, self.T, self.K = 10, 4, 500, 1
                self.A = [1] * 10
                self.C = [[10] * 10 for _ in range(4)]
                return

            self.N, self.L, self.T, self.K = map(int, line1)
            # 2行目: Level 0 の生産能力 A
            self.A = list(map(int, sys.stdin.readline().split()))
            # 3行目以降: 各Levelの初期コスト C
            self.C = []
            for _ in range(self.L):
                self.C.append(list(map(int, sys.stdin.readline().split())))
        except ValueError:
            sys.exit(0)

DATA = ProblemData()

class Simulation:
    """シミュレーションを行うクラス"""
    
    @staticmethod
    def run_greedy_logic() -> List[Tuple[int, int]]:
        """
        むつきさん提示の貪欲法ロジックを実行し、
        「どのような順番で何を買ったか」のリストを生成して返す。
        """
        # シミュレーション用変数
        current_apples = DATA.K
        B = [[1] * DATA.N for _ in range(DATA.L)]
        P = [[0] * DATA.N for _ in range(DATA.L)]
        
        operation_log = [] # (Level, ID) の順番リスト

        for t in range(DATA.T):
            action_i = -1
            action_j = -1
            
            # --- 戦略A: ID=0 の高レベル優先 ---
            found_high_level = False
            target_id = 0
            for i in range(DATA.L - 1, 0, -1): # 3, 2, 1
                cost = DATA.C[i][target_id] * (P[i][target_id] + 1)
                if current_apples >= cost:
                    action_i = i
                    action_j = target_id
                    current_apples -= cost
                    P[i][target_id] += 1
                    found_high_level = True
                    break
            
            # --- 戦略B: コスパ探索 ---
            if not found_high_level:
                best_efficiency = -1.0
                best_j = -1
                for j in range(DATA.N):
                    cost = DATA.C[0][j] * (P[0][j] + 1)
                    if current_apples < cost:
                        continue
                    # 効率 = 増分 / コスト (増分は A[j] * B[0][j])
                    gain = DATA.A[j] * B[0][j]
                    efficiency = gain / cost
                    
                    if efficiency > best_efficiency:
                        best_efficiency = efficiency
                        best_j = j
                
                if best_j != -1:
                    action_i = 0
                    action_j = best_j
                    current_apples -= DATA.C[0][best_j] * (P[0][best_j] + 1)
                    P[0][best_j] += 1
            
            # 操作があれば記録
            if action_i != -1:
                operation_log.append((action_i, action_j))
            
            # 生産処理
            # Level 0
            prod_l0 = 0
            for j in range(DATA.N):
                if P[0][j] > 0:
                    prod_l0 += DATA.A[j] * B[0][j] * P[0][j]
            current_apples += prod_l0
            
            # Level 1..3
            for i in range(1, DATA.L):
                for j in range(DATA.N):
                    if P[i][j] > 0:
                        B[i-1][j] += B[i][j] * P[i][j]
                        
        return operation_log

    @staticmethod
    def evaluate(ops: List[Tuple[int, int]]) -> float:
        """
        操作リスト ops に従ってシミュレーションを行い、最終りんご数を返す
        """
        B = [[1] * DATA.N for _ in range(DATA.L)]
        P = [[0] * DATA.N for _ in range(DATA.L)]
        apples = float(DATA.K)
        
        ops_idx = 0
        ops_len = len(ops)
        
        # 配列アクセスを高速化するためにローカル変数化
        T = DATA.T
        N = DATA.N
        L = DATA.L
        DataA = DATA.A
        DataC = DATA.C
        
        for t in range(T):
            # 1. 購入フェーズ
            if ops_idx < ops_len:
                lvl, mid = ops[ops_idx]
                cost = DataC[lvl][mid] * (P[lvl][mid] + 1)
                
                if apples >= cost:
                    apples -= cost
                    P[lvl][mid] += 1
                    ops_idx += 1
                # 買えない場合はスキップ（次のターン以降に持ち越し）
            
            # 2. 生産フェーズ
            # Level 0
            prod = 0
            # P[0]を見て計算
            p0 = P[0]
            b0 = B[0]
            for j in range(N):
                if p0[j] > 0:
                    prod += DataA[j] * b0[j] * p0[j]
            apples += prod
            
            # Level 1..L-1
            for i in range(1, L):
                pi = P[i]
                bi = B[i]
                bi_prev = B[i-1]
                for j in range(N):
                    if pi[j] > 0:
                        bi_prev[j] += bi[j] * pi[j]
                        
        return apples

def is_valid_sequence(ops: List[Tuple[int, int]]) -> bool:
    """
    制約チェック:
    ID=0, Level=1 の機械を購入した以降は、ID=0 以外の機械が含まれていてはならない。
    """
    trigger_found = False
    
    for lvl, mid in ops:
        if trigger_found:
            # トリガー後は ID=0 以外禁止
            if mid != 0:
                return False
        else:
            # トリガー判定: Level 1 かつ ID 0
            if lvl == 1 and mid == 0:
                trigger_found = True
                
    return True

def solve():
    start_time = time.time()
    
    # 1. 初期解の生成（貪欲法ベース）
    initial_ops = Simulation.run_greedy_logic()
    
    # 初期解が制約を満たしているか確認（念のため）
    # 満たしていない場合は、制約に合うように後ろを削るなどの処理が必要だが、
    # 貪欲法のロジック上、ID0の強化が進むはずなので概ね大丈夫と仮定。
    # もし違反していれば修正する。
    if not is_valid_sequence(initial_ops):
        # 修正: 最初の (1,0) 以降の非ID0を削除
        fixed_ops = []
        trigger = False
        for lvl, mid in initial_ops:
            if trigger:
                if mid == 0:
                    fixed_ops.append((lvl, mid))
            else:
                fixed_ops.append((lvl, mid))
                if lvl == 1 and mid == 0:
                    trigger = True
        initial_ops = fixed_ops

    current_ops = initial_ops[:]
    current_score = Simulation.evaluate(current_ops)
    
    best_ops = current_ops[:]
    best_score = current_score
    
    # ログ出力
    sys.stderr.write(f"# Initial Greedy Score: {best_score:.4e}\n")
    
    # --- 焼きなましパラメータ ---
    # 生のスコア（非常に大きい）を使うため、温度も大きく設定
    # 桁数が大きいので対数温度管理などが理想だが、簡易的に大きな値からスタート
    T0 = 1e15  # 初期温度（かなり適当だが大きく）
    T1 = 1e5   # 終端温度
    temperature = T0
    loop_count = 0
    
    while True:
        loop_count += 1
        
        if loop_count % LOG_INTERVAL == 0:
            now = time.time()
            # ログ出力
            sys.stderr.write(f"# Loop: {loop_count}, Best: {best_score:.4e}, Time: {now-start_time:.2f}s\n")
            
            if now - start_time > TIME_LIMIT:
                break
            
            # 温度更新
            progress = (now - start_time) / TIME_LIMIT
            # 指数的な冷却、あるいは線形で十分
            temperature = T0 ** (1 - progress) * T1 ** progress

        # --- 近傍操作 ---
        # リストのコピーを作成
        neighbor_ops = current_ops[:]
        
        mode = random.random()
        ops_len = len(neighbor_ops)
        
        if mode < 0.4: # 追加 (Add)
            # どこに何を追加するか
            pos = random.randint(0, ops_len) # 末尾も含む
            
            # 制約を考慮して追加するIDを決める
            # 簡易的に: ランダムに作って、後で valid check する方式だと効率が悪いので、
            # 「生成時点でなるべく valid にする」
            
            # 挿入位置より前に (1,0) があるか？
            has_trigger_before = False
            for k in range(min(pos, len(neighbor_ops))):
                if neighbor_ops[k] == (1, 0):
                    has_trigger_before = True
                    break
            
            if has_trigger_before:
                # 前にトリガーがあるなら、追加できるのは ID=0 のみ
                new_id = 0
                new_lvl = random.randint(0, DATA.L - 1)
            else:
                # 前にトリガーがない場合
                # IDは何でもいいが、もし (1,0) を追加すると後ろとの整合性が崩れる可能性がある
                # 安全策: ここでは (1,0) 以外を追加するか、単純にランダムにして is_valid で弾く
                # 効率重視で、ID0以外も許可するが、(1,0) は慎重に扱う
                new_lvl = random.randint(0, DATA.L - 1)
                new_id = random.randint(0, DATA.N - 1)
            
            neighbor_ops.insert(pos, (new_lvl, new_id))

        elif mode < 0.7: # 削除 (Delete)
            if ops_len > 0:
                pos = random.randint(0, ops_len - 1)
                # 削除は制約を壊さない（「ID0以外禁止」の区間にゴミが残ることはない）
                # ただし、(1,0) を消すと、その後の ID!=0 が許可されるようになる（制約緩和）のでOK
                neighbor_ops.pop(pos)
                
        elif mode < 0.9: # 変更 (Change)
            if ops_len > 0:
                pos = random.randint(0, ops_len - 1)
                
                # 変更も制約チェックが必要
                # 面倒なのでランダム変更 -> チェックではじく
                new_lvl = random.randint(0, DATA.L - 1)
                new_id = random.randint(0, DATA.N - 1)
                neighbor_ops[pos] = (new_lvl, new_id)
                
        else: # 交換 (Swap)
            if ops_len >= 2:
                p1 = random.randint(0, ops_len - 1)
                p2 = random.randint(0, ops_len - 1)
                neighbor_ops[p1], neighbor_ops[p2] = neighbor_ops[p2], neighbor_ops[p1]

        # --- 制約チェック (必須) ---
        if not is_valid_sequence(neighbor_ops):
            continue

        # --- 評価 ---
        new_score = Simulation.evaluate(neighbor_ops)
        delta = new_score - current_score
        
        if delta > 0:
            current_ops = neighbor_ops
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_ops = neighbor_ops[:] # Deep Copy
        else:
            # 確率遷移
            # 温度が高いときは delta が大きくても許容
            # delta は負の値 (e.g. -10000)
            try:
                prob = math.exp(delta / temperature)
            except OverflowError:
                prob = 0
            
            if random.random() < prob:
                current_ops = neighbor_ops
                current_score = new_score

    # --- 結果出力 ---
    # 最終的な best_ops に基づいて出力
    output_schedule(best_ops)

def output_schedule(ops: List[Tuple[int, int]]):
    """最終的な操作リストに従って出力を行う"""
    B = [[1] * DATA.N for _ in range(DATA.L)]
    P = [[0] * DATA.N for _ in range(DATA.L)]
    apples = DATA.K
    
    ops_idx = 0
    ops_len = len(ops)
    
    for t in range(DATA.T):
        did_action = False
        if ops_idx < ops_len:
            lvl, mid = ops[ops_idx]
            cost = DATA.C[lvl][mid] * (P[lvl][mid] + 1)
            
            if apples >= cost:
                print(f"{lvl} {mid}")
                apples -= cost
                P[lvl][mid] += 1
                ops_idx += 1
                did_action = True
        
        if not did_action:
            print("-1")
            
        # 生産 (計算は不要だが、内部状態合わせのために記述してもよい。
        # 今回は出力だけなら不要だが、変数を更新しないと次のコスト計算が狂うので必要)
        
        # Level 0
        prod_l0 = 0
        for j in range(DATA.N):
            if P[0][j] > 0:
                prod_l0 += DATA.A[j] * B[0][j] * P[0][j]
        apples += prod_l0
        
        # Level 1..L-1
        for i in range(1, DATA.L):
            for j in range(DATA.N):
                if P[i][j] > 0:
                    B[i-1][j] += B[i][j] * P[i][j]

if __name__ == "__main__":
    solve()