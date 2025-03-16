import numpy as np
import random
import time

def solve_cleaning_duty_simulated_annealing(N, L, T):
    """
    焼きなまし法を用いた掃除当番最適化
    N: 社員数
    L: 週数
    T: 各社員の掃除当番回数の目標値
    """
    # 初期温度と冷却率
    temperature = 10.0
    cooling_rate = 0.85
    
    # 最大試行回数（実行時間制限のため調整）
    max_iterations = 30
    
    # 初期解をランダムに生成
    current_a = np.random.randint(0, N, size=N)
    current_b = np.random.randint(0, N, size=N)
    
    # 重要度の高い社員（目標値が大きい社員）に対して初期解を改善
    sorted_indices = np.argsort(T)[::-1]  # 目標値が大きい順
    for idx in sorted_indices[:20]:  # 上位20人のみ最適化
        if T[idx] > L / N:
            potential_targets = [j for j in range(N) if T[j] >= T[idx] * 0.7]
            if potential_targets:
                current_a[idx] = random.choice(potential_targets)
                current_b[idx] = random.choice(potential_targets)
    
    # 初期解の評価
    current_error = evaluate_solution(N, L, current_a, current_b, T)
    
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
        
        # ランダムに一部の遷移を変更
        num_changes = max(1, int(N * (1 - iteration / max_iterations) * 0.1))  # 徐々に変更量を減らす
        for _ in range(num_changes):
            i = random.randint(0, N-1)
            if random.random() < 0.5:
                new_a[i] = random.randint(0, N-1)
            else:
                new_b[i] = random.randint(0, N-1)
        
        # 新しい解を評価
        new_error = evaluate_solution(N, L, new_a, new_b, T)
        
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
    
    return best_a, best_b, best_error

def evaluate_solution(N, L, a, b, T, max_weeks=1000):
    """
    解の評価（高速化のため、シミュレーション期間を短縮して近似）
    """
    # シミュレーション期間を短縮（全期間のシミュレーションだと時間がかかりすぎる）
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