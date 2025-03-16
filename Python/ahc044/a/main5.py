import numpy as np
import random
import time

def solve_cleaning_duty_simulated_annealing(N, L, T):
    """
    焼きなまし法を用いた掃除当番最適化
    誤差の大きい社員を優先的に修正
    """
    # 初期温度と冷却率
    temperature = 20.0
    cooling_rate = 0.9
    
    # 最大試行回数
    max_iterations = 1000
    
    # 確率分布を作成（T_i/Lの確率で社員iを選ぶ）
    probabilities = np.array(T) / L
    
    # 初期解をT_i/Lの確率分布に基づいて生成
    current_a = np.zeros(N, dtype=int)
    current_b = np.zeros(N, dtype=int)
    
    for i in range(N):
        # 確率分布に基づいて社員を選択
        current_a[i] = np.random.choice(N, p=probabilities)
        current_b[i] = np.random.choice(N, p=probabilities)
    
    # 初期解の評価
    current_error, current_errors = evaluate_solution_probabilistic(N, L, current_a, current_b, T)
    
    # 最良解を記録
    best_a = current_a.copy()
    best_b = current_b.copy()
    best_error = current_error
    best_errors = current_errors.copy()
    
    # 開始時刻
    start_time = time.time()
    
    # 焼きなまし法のメインループ
    for iteration in range(max_iterations):
        # 実行時間をチェック（1.8秒を超えたら終了）
        if time.time() - start_time > 1.8:
            break
        
        # 温度を下げる
        temperature *= cooling_rate
        
        # 新しい解を生成（近傍解）
        new_a = current_a.copy()
        new_b = current_b.copy()
        
        # 変更する要素数を決定（徐々に減少）
        num_changes = max(1, int(N * (1 - iteration / max_iterations) * 0.1))
        
        # 誤差の大きい社員を優先的に選択して修正
        error_indices = np.argsort(current_errors)[::-1]  # 誤差が大きい順
        selected_indices = error_indices[:num_changes * 2]  # 十分な候補を選択
        
        # 選択した社員のうちランダムにnum_changes個を実際に修正
        change_indices = np.random.choice(selected_indices, size=min(num_changes, len(selected_indices)), replace=False)
        
        for i in change_indices:
            if current_errors[i] > 0:  # 誤差がある場合のみ修正
                # 現在の割り当て回数と目標値の差を考慮
                if random.random() < 0.5:
                    # a[i]を修正
                    if current_errors[i] > 0:  # 割り当てすぎ
                        # 割り当て不足の社員を優先
                        candidates = [j for j in range(N) if current_errors[j] < 0]
                        if candidates:
                            new_a[i] = random.choice(candidates)
                        else:
                            new_a[i] = np.random.choice(N, p=probabilities)
                    else:  # 割り当て不足
                        # 割り当てすぎの社員を優先
                        candidates = [j for j in range(N) if current_errors[j] > 0]
                        if candidates:
                            new_a[i] = random.choice(candidates)
                        else:
                            new_a[i] = np.random.choice(N, p=probabilities)
                else:
                    # b[i]を修正（同様のロジック）
                    if current_errors[i] > 0:  # 割り当てすぎ
                        candidates = [j for j in range(N) if current_errors[j] < 0]
                        if candidates:
                            new_b[i] = random.choice(candidates)
                        else:
                            new_b[i] = np.random.choice(N, p=probabilities)
                    else:  # 割り当て不足
                        candidates = [j for j in range(N) if current_errors[j] > 0]
                        if candidates:
                            new_b[i] = random.choice(candidates)
                        else:
                            new_b[i] = np.random.choice(N, p=probabilities)
        
        # 新しい解を評価
        new_error, new_errors = evaluate_solution_probabilistic(N, L, new_a, new_b, T)
        
        # 解を受理するかどうか決定
        if accept_solution(current_error, new_error, temperature):
            current_a = new_a.copy()
            current_b = new_b.copy()
            current_error = new_error
            current_errors = new_errors.copy()
            
            # 最良解の更新
            if new_error < best_error:
                best_a = new_a.copy()
                best_b = new_b.copy()
                best_error = new_error
                best_errors = new_errors.copy()
    
    # 最適化の最後に短いシミュレーションで最良解をチェック
    simulated_error = evaluate_solution_simulation(N, L, best_a, best_b, T, max_weeks=1000)
    
    # 最終調整（時間があれば）
    if time.time() - start_time < 1.7:
        best_a, best_b = final_adjustment(N, L, best_a, best_b, T, best_errors)
    
    return best_a, best_b, simulated_error

def evaluate_solution_probabilistic(N, L, a, b, T):
    """
    確率的モデルによる高速評価
    マルコフ連鎖の定常分布を計算して誤差を推定
    """
    # 遷移行列の構築
    transition_matrix = np.zeros((N, N))
    
    for i in range(N):
        # 奇数回の場合: a[i]に移動
        # 偶数回の場合: b[i]に移動
        # 平均すると各方向に50%ずつ遷移すると仮定
        transition_matrix[i, a[i]] += 0.5
        transition_matrix[i, b[i]] += 0.5
    
    # 初期状態ベクトル（社員0からスタート）
    state_vector = np.zeros(N)
    state_vector[0] = 1.0
    
    # パワー法による定常分布の近似計算
    num_iterations = 30
    for _ in range(num_iterations):
        state_vector = np.dot(state_vector, transition_matrix)
    
    # 定常分布を使って各社員の出現頻度を予測
    predicted_count = state_vector * L
    
    # 誤差計算（全体の誤差と各社員ごとの誤差）
    errors = predicted_count - T  # 正の値は割り当てすぎ、負の値は割り当て不足
    total_error = np.sum(np.abs(errors))
    
    return total_error, errors

def evaluate_solution_simulation(N, L, a, b, T, max_weeks=1000):
    """
    シミュレーションによる評価（最終確認用）
    """
    # シミュレーション期間を短縮
    sim_weeks = min(max_weeks, L)
    
    # シミュレーション実行
    count = np.zeros(N, dtype=int)
    current = 0  # 最初は社員0
    
    for _ in range(sim_weeks):
        count[current] += 1
        if count[current] % 2 == 1:  # 奇数回目
            current = a[current]
        else:  # 偶数回目
            current = b[current]
    
    # 結果を全期間に拡大
    if sim_weeks < L:
        count = count * (L / sim_weeks)
    
    # 誤差計算
    error = np.sum(np.abs(count - T))
    return error

def accept_solution(current_error, new_error, temperature):
    """
    焼きなまし法の受理判定
    """
    if new_error < current_error:
        return True
    else:
        # 確率的に悪い解も受理
        probability = np.exp((current_error - new_error) / temperature)
        return random.random() < probability

def final_adjustment(N, L, a, b, T, errors):
    """
    最終的な調整：誤差が最も大きい社員を集中的に修正
    """
    # 誤差の絶対値が大きい順に社員をソート
    worst_indices = np.argsort(np.abs(errors))[::-1][:15]  # 上位15人
    
    # 各社員について個別に調整
    for idx in worst_indices:
        if errors[idx] > 0:  # 割り当てすぎ
            # この社員に向かう遷移を減らす
            incoming = []
            for j in range(N):
                if a[j] == idx:
                    incoming.append((j, 'a'))
                if b[j] == idx:
                    incoming.append((j, 'b'))
            
            if incoming:
                # 誤差の大きさに比例して複数の遷移を修正
                num_changes = min(3, len(incoming))
                selected = random.sample(incoming, num_changes)
                
                for j, which in selected:
                    # 割り当て不足の社員を優先的に選択
                    candidates = [k for k in range(N) if errors[k] < 0]
                    if candidates:
                        if which == 'a':
                            a[j] = random.choice(candidates)
                        else:
                            b[j] = random.choice(candidates)
        else:  # 割り当て不足
            # この社員に向かう遷移を増やす
            num_changes = min(3, N // 10)
            for _ in range(num_changes):
                j = random.choice(range(N))
                if random.random() < 0.5:
                    a[j] = idx
                else:
                    b[j] = idx
    
    return a, b

def main():
    # 入力読み込み
    N, L = map(int, input().split())
    T = list(map(int, input().split()))
    
    # 問題を解く
    a, b, _ = solve_cleaning_duty_simulated_annealing(N, L, T)
    
    # 結果を出力
    for i in range(N):
        print(f"{a[i]} {b[i]}")

if __name__ == "__main__":
    main()