import sys
import random
import math
import time

def main():
    """
    メイン関数: 入力の受け取りと、操作手順リストに対する焼きなまし法(SA)を実行する。
    """
    # --- 時間管理 ---
    start_time = time.time()
    TIME_LIMIT = 1.8 # Pythonでの安全な制限時間

    # (本来はここで入力の受け取りと初期盤面の構築を行います)
    # N = int(input())
    # ... (むつきの既存のインフラ構築コードをここに統合します) ...

    # ダミーデータ (実際の変数はむつきの環境に合わせてください)
    MAX_TURNS = 2000
    current_ops = generate_initial_solution(MAX_TURNS)
    
    # --- 焼きなまし法の初期化 ---
    current_score = evaluate_operations(current_ops)
    best_ops = current_ops[:]
    best_score = current_score

    T0 = 10000.0  # 初期温度 (序盤は大きく改悪する手も許容)
    T1 = 10.0     # 最終温度 (終盤は改善する手のみ採用)
    
    iter_count = 0

    # --- 焼きなまし法の核心部: メインループ ---
    while True:
        now_time = time.time()
        elapsed = now_time - start_time
        if elapsed > TIME_LIMIT:
            break
            
        iter_count += 1
        
        # 指数冷却による現在の温度計算
        temp = T0 * ((T1 / T0) ** (elapsed / TIME_LIMIT))

        # --- 焼きなまし法の核心部: 近傍操作 ---
        new_ops = current_ops[:]
        op_type = random.random()
        
        if op_type < 0.5:
            # 1. 変更 (Modify): ランダムな位置の操作を書き換える
            idx = random.randint(0, len(new_ops) - 1)
            new_ops[idx] = (random.randint(0, 19), random.choice([-1, 1]))
        elif op_type < 0.8:
            # 2. スワップ (Swap): 隣接する操作を入れ替える
            idx = random.randint(0, len(new_ops) - 2)
            new_ops[idx], new_ops[idx+1] = new_ops[idx+1], new_ops[idx]
        else:
            # 3. 削除＆末尾追加 (Shift): 途中の無駄を消し、手数を詰める
            idx = random.randint(0, len(new_ops) - 1)
            new_ops.pop(idx)
            new_ops.append((random.randint(0, 19), random.choice([-1, 1])))

        # 新しい手順の評価
        new_score = evaluate_operations(new_ops)

        # --- 焼きなまし法の核心部: 遷移確率の判定 ---
        diff = new_score - current_score
        
        # 評価が良くなった場合、または温度に基づく確率で改悪を許容する場合に状態を更新
        if diff >= 0 or random.random() < math.exp(diff / temp):
            current_ops = new_ops
            current_score = new_score
            
            # 歴代ベストの更新
            if current_score > best_score:
                best_score = current_score
                best_ops = current_ops[:]

    # 結果出力
    print(f"# SA Iterations: {iter_count}, Best Score: {best_score}", file=sys.stderr)
    print(len(best_ops))
    for m, d in best_ops:
        print(f"{m} {d}")


def generate_initial_solution(length: int) -> list:
    """
    初期解を生成する関数。
    最初はランダム、または貧弱な貪欲法の出力結果を初期解として与えるとSAが効率的に進みます。
    """
    return [(random.randint(0, 19), random.choice([-1, 1])) for _ in range(length)]


def evaluate_operations(ops: list) -> float:
    """
    与えられた操作手順リスト(ops)を最初からシミュレーションし、最終盤面の良さを評価する。
    """
    # 盤面のコピーを作成 (シミュレーション用)
    # current_grid = initial_grid.copy()
    
    score = 0.0
    exported_count = 0
    target = 0
    
    # 1. 操作のシミュレーション
    for m, d in ops:
        # apply_action(current_grid, m, d) # 盤面を更新
        # もし target が搬出口に到達したら、exported_count と target を +1
        pass
        
    # --- 評価関数の核心部 ---
    # 1. 搬出数の絶対評価 (最優先)
    score += exported_count * 1000000.0
    
    # 2. 列車組み立て評価 (局所的な整頓を大域的最適化に繋げる)
    # for each conveyor:
    #     for each position i:
    #         if current_grid[i] != -1 and current_grid[i] + 1 == current_grid[i+1]:
    #             score += 50000.0 # 順番通りに並んでいれば特大ボーナス！
                
    return score

if __name__ == "__main__":
    main()