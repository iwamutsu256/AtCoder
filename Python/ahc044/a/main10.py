import numpy as np
import random
import time

def solve_cleaning_duty_simulated_annealing_v5(N, L, T):
    """
    焼きなまし法を用いた掃除当番最適化 (誤差が大きい社員に着目した近傍探索 - ベースコード改造版)
    N: 社員数
    L: 週数
    T: 各社員の掃除当番回数の目標値
    """
    # 初期温度と冷却率
    temperature = 10.0
    cooling_rate = 0.97  # 冷却率を0.97に変更

    # 最大試行回数
    max_iterations = 250  # ループ回数を増やす

    # 確率分布を作成（T_i/Lの確率で社員iを選ぶ）
    probabilities = np.array(T) / L

    # 初期解をT_i/Lの確率分布に基づいて生成
    current_a = np.zeros(N, dtype=int)
    current_b = np.zeros(N, dtype=int)

    for i in range(N):
        current_a[i] = np.random.choice(N, p=probabilities)
        current_b[i] = np.random.choice(N, p=probabilities)

    # 初期解の評価 (マルコフ連鎖評価に変更)
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

        # 近傍探索：誤差が大きい社員に着目 (ソートを避ける)
        current_counts = calculate_estimated_counts(N, L, current_a, current_b)
        errors = np.abs(current_counts - T)

        # 誤差が大きい社員をランダムに選択 (ソートの代わりにランダムサンプリング)
        num_worst = min(5, N)  # 誤差が大きい上位数名
        worst_candidates_indices = np.argpartition(errors, -num_worst)[-num_worst:]
        target_employee = random.choice(worst_candidates_indices)

        # 誤差が大きい社員に関連する遷移を変更
        changing_employee = random.randint(0, N - 1)

        if random.random() < 0.7:
            # 目標回数より少ない社員への遷移を増やす
            candidate_targets = np.where(current_counts < T)[0]
            if len(candidate_targets) > 0:
                if random.random() < 0.5:
                    new_a[changing_employee] = random.choice(candidate_targets)
                else:
                    new_b[changing_employee] = random.choice(candidate_targets)
            else:
                # 目標回数より少ない社員がいない場合はランダムな遷移
                if random.random() < 0.5:
                    new_a[changing_employee] = np.random.choice(N, p=probabilities)
                else:
                    new_b[changing_employee] = np.random.choice(N, p=probabilities)
        else:
            # ランダムな変更も行う
            if random.random() < 0.5:
                new_a[changing_employee] = np.random.choice(N, p=probabilities)
            else:
                new_b[changing_employee] = np.random.choice(N, p=probabilities)

        # 新しい解の評価 (マルコフ連鎖評価)
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

    # 最終調整（最も誤差の大きい社員を修正）
    best_a, best_b = final_adjustment(N, L, best_a, best_b, T)

    return best_a, best_b, best_error

def calculate_estimated_counts(N, L, a, b):
    """
    簡易的なシミュレーションで各社員の出現回数を計算
    """
    count = np.zeros(N, dtype=int)
    current = 0
    for _ in range(1000):
        count[current] += 1
        if count[current] % 2 == 1:
            current = a[current]
        else:
            current = b[current]
    return count * (L / 1000)

def evaluate_solution_probabilistic(N, L, a, b, T):
    """
    確率的なマルコフ連鎖を用いて解の評価を行う
    """
    transition_matrix = np.zeros((N, N))

    # 遷移行列を作成 (奇数回 a[i], 偶数回 b[i])
    for i in range(N):
        transition_matrix[i, a[i]] += 0.5
        transition_matrix[i, b[i]] += 0.5

    # 初期状態ベクトル (社員0からスタート)
    state_vector = np.zeros(N)
    state_vector[0] = 1.0

    # パワー法による定常分布の計算 (20回反復)
    for _ in range(15):
        state_vector = np.dot(state_vector, transition_matrix)

    # 各社員の掃除回数を推定
    predicted_count = state_vector * L
    error = np.sum(np.abs(predicted_count - T))

    return error

def accept_solution(current_error, new_error, temperature):
    """
    焼きなまし法の受理判定
    """
    if new_error < current_error:
        return True
    probability = np.exp((current_error - new_error) / temperature)
    return random.random() < probability

def final_adjustment(N, L, a, b, T):
    """
    最終的な調整：最も誤差の大きい社員を修正
    """
    count = np.zeros(N, dtype=int)
    current = 0
    for _ in range(1000):
        count[current] += 1
        if count[current] % 2 == 1:
            current = a[current]
        else:
            current = b[current]

    estimated_count = count * (L / 1000)
    errors = np.abs(estimated_count - T)

    worst_indices = np.argsort(errors)[-10:]
    probabilities = np.array(T) / L

    for idx in worst_indices:
        diff = estimated_count[idx] - T[idx]
        if diff > 0:
            incoming = [j for j in range(N) if a[j] == idx or b[j] == idx]
            if incoming:
                j = random.choice(incoming)
                if a[j] == idx:
                    a[j] = np.random.choice(N, p=probabilities)
                if b[j] == idx:
                    b[j] = np.random.choice(N, p=probabilities)
        else:
            j = random.choice(range(N))
            if random.random() < 0.5:
                a[j] = idx
            else:
                b[j] = idx

    return a, b

def main():
    N, L = map(int, input().split())
    T = list(map(int, input().split()))

    a, b, _ = solve_cleaning_duty_simulated_annealing_v5(N, L, T)

    for i in range(N):
        print(f"{a[i]} {b[i]}")

if __name__ == "__main__":
    main()