import numpy as np
import random
import time

def solve_cleaning_duty_simulated_annealing(N, L, T):
    """
    焼きなまし法を用いた掃除当番最適化
    確率的モデルによる高速評価を実装
    """
    # 初期温度と冷却率
    temperature = 20.0
    cooling_rate = 0.9
    
    # 最大試行回数（高速化により増加可能）
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
    
    # 初期解の評価（確率的評価）
    current_error = evaluate_solution_probabilistic(N, L, current_a, current_b, T)
    
    # 最良解を記録
    best_a = current_a.copy()
    best_b = current_b.copy()
    best_error = current_error
    
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
        
        # ランダムに一部の遷移を変更
        for _ in range(num_changes):
            i = random.randint(0, N-1)
            if random.random() < 0.5:
                # 確率分布に基づいて選択
                new_a[i] = np.random.choice(N, p=probabilities)
            else:
                new_b[i] = np.random.choice(N, p=probabilities)
        
        # 新しい解を評価（確率的評価）
        new_error = evaluate_solution_probabilistic(N, L, new_a, new_b, T)
        
        # 解を受理するかどうか決定
        if accept_solution(current_error, new_error, temperature):
            current_a = new_a.copy()
            current_b = new_b.copy()
            current_error = new_error
            
            # 最良解の更新
            if new_error < best_error:
                best_a = new_a.copy()
                best_b = new_b.copy()
                best_error = new_error
    
    # 最適化の最後に短いシミュレーションで最良解をチェック
    simulated_error = evaluate_solution_simulation(N, L, best_a, best_b, T, max_weeks=1000)
    
    # 最終調整（時間があれば）
    if time.time() - start_time < 1.7:
        best_a, best_b = final_adjustment(N, L, best_a, best_b, T)
    
    return best_a, best_b, simulated_error

def evaluate_solution_probabilistic(N, L, a, b, T):
    """
    確率的モデルによる高速評価
    マルコフ連鎖の定常分布を近似計算して誤差を推定
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
    num_iterations = 50  # 少ない反復回数で近似
    for _ in range(num_iterations):
        state_vector = np.dot(state_vector, transition_matrix)
    
    # 定常分布を使って各社員の出現頻度を予測
    predicted_count = state_vector * L
    
    # 誤差計算
    error = np.sum(np.abs(predicted_count - T))
    return error

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

def final_adjustment(N, L, a, b, T):
    """
    最終的な調整
    """
    # マルコフ連鎖による定常分布の計算
    transition_matrix = np.zeros((N, N))
    for i in range(N):
        transition_matrix[i, a[i]] += 0.5
        transition_matrix[i, b[i]] += 0.5
    
    state_vector = np.zeros(N)
    state_vector[0] = 1.0
    
    for _ in range(50):
        state_vector = np.dot(state_vector, transition_matrix)
    
    predicted_count = state_vector * L
    
    # 誤差計算
    errors = np.abs(predicted_count - T)
    
    # 最も誤差の大きい社員TOP10を特定
    worst_indices = np.argsort(errors)[-10:]
    
    # 確率分布
    probabilities = np.array(T) / L
    
    # 誤差の大きい社員の割り当てを調整
    for idx in worst_indices:
        diff = predicted_count[idx] - T[idx]
        if diff > 0:  # 割り当てすぎ
            # この社員に向かう遷移を減らす
            incoming = []
            for j in range(N):
                if a[j] == idx:
                    incoming.append((j, 'a'))
                if b[j] == idx:
                    incoming.append((j, 'b'))
            
            if incoming:
                j, which = random.choice(incoming)
                if which == 'a':
                    # この社員より少ない目標値を持つ社員へ変更
                    candidates = [k for k in range(N) if T[k] < T[idx]]
                    if candidates:
                        a[j] = random.choice(candidates)
                    else:
                        a[j] = np.random.choice(N, p=probabilities)
                else:
                    candidates = [k for k in range(N) if T[k] < T[idx]]
                    if candidates:
                        b[j] = random.choice(candidates)
                    else:
                        b[j] = np.random.choice(N, p=probabilities)
        else:  # 割り当て不足
            # この社員に向かう遷移を増やす
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