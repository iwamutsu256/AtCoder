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
    max_iterations = 100
    
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
        num_changes = max(1, int(N * (1 - iteration / max_iterations) * 0.1))
        for _ in range(num_changes):
            i = random.randint(0, N-1)
            if random.random() < 0.5:
                # 確率分布に基づいて選択
                new_a[i] = np.random.choice(N, p=probabilities)
            else:
                new_b[i] = np.random.choice(N, p=probabilities)
        
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
    
    # 最終的な調整（最も誤差の大きい社員を修正）
    best_a, best_b = final_adjustment(N, L, best_a, best_b, T)
    
    return best_a, best_b, best_error

def evaluate_solution(N, L, a, b, T, max_weeks=1000):
    """
    解の評価（高速化のため、シミュレーション期間を短縮して近似）
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
    最終的な調整：最も誤差の大きい社員について調整を行う
    """
    # 簡易的なシミュレーションで各社員の出現回数を計算
    count = np.zeros(N, dtype=int)
    current = 0
    for _ in range(1000):  # 短いシミュレーション
        count[current] += 1
        if count[current] % 2 == 1:
            current = a[current]
        else:
            current = b[current]
    
    # 全期間の推定出現回数
    estimated_count = count * (L / 1000)
    
    # 誤差計算
    errors = np.abs(estimated_count - T)
    
    # 最も誤差の大きい社員TOP10を特定
    worst_indices = np.argsort(errors)[-10:]
    
    # 確率分布
    probabilities = np.array(T) / L
    
    # 最も誤差の大きい社員の割り当てを調整
    for idx in worst_indices:
        diff = estimated_count[idx] - T[idx]
        if diff > 0:  # 割り当てすぎ
            # この社員に向かう遷移を減らす
            incoming = [j for j in range(N) if a[j] == idx or b[j] == idx]
            if incoming:
                j = random.choice(incoming)
                if a[j] == idx:
                    a[j] = np.random.choice(N, p=probabilities)
                if b[j] == idx:
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