import sys

def main():
    """
    メイン関数: 入力の受け取り、解法の実行、結果の出力を行う。
    """
    # Nは20で固定
    N = int(input())
    
    # a: 倉庫の初期状態 (20x20)
    a = []
    for _ in range(N):
        row = list(map(int, input().split()))
        a.append(row)
        
    # ハミルトン閉路（一筆書き）のルートを作成する
    loop_path = create_hamiltonian_cycle(N)
    
    # 設置するコンベアは1つだけ
    M = 1
    
    # コンベアの出力情報の構築
    # 形式: length i0 j0 i1 j1 ...
    conveyor_out = [len(loop_path)]
    for r, c in loop_path:
        conveyor_out.extend([r, c])
        
    print(M)
    print(*conveyor_out)
    
    # --- 貪欲法: ここから箱の回収シミュレーション ---
    # 箱の初期位置（ループ上のインデックス）を記録
    box_to_initial_idx = {}
    exit_idx = -1 # 搬出口 (0, N//2) のループ上のインデックス
    
    for idx, (r, c) in enumerate(loop_path):
        box_id = a[r][c]
        box_to_initial_idx[box_id] = idx
        if r == 0 and c == N // 2:
            exit_idx = idx

    operations = []
    # 現在のループのズレ（コンベアを回した量）を管理
    current_offset = 0 
    
    # 箱0から(N*N - 1)まで順番に搬出する
    for target_box in range(N * N):
        # ターゲットの箱の、初期状態でのインデックス
        init_idx = box_to_initial_idx[target_box]
        
        # --- 貪欲法の核心部: 最短操作の選択 ---
        # ターゲットの箱の現在のインデックスを計算
        current_idx = (init_idx + current_offset) % len(loop_path)
        
        # 搬出口までの差分（正方向・逆方向）を計算
        diff_forward = (exit_idx - current_idx) % len(loop_path)
        diff_backward = (current_idx - exit_idx) % len(loop_path)
        
        # 距離が短い方向を選ぶ
        if diff_forward == 0:
            # 既に搬出口にある場合は動かす必要なし（自動的に搬出される）
            pass
        elif diff_forward <= diff_backward:
            # 正方向に動かす
            for _ in range(diff_forward):
                operations.append((0, 1)) # コンベア0を方向1へ
            current_offset = (current_offset + diff_forward) % len(loop_path)
        else:
            # 逆方向に動かす
            for _ in range(diff_backward):
                operations.append((0, -1)) # コンベア0を方向-1へ
            current_offset = (current_offset - diff_backward) % len(loop_path)

    # 操作結果の出力
    print(len(operations))
    for m, d in operations:
        print(f"{m} {d}")


def create_hamiltonian_cycle(N: int) -> list[tuple[int, int]]:
    """
    NxNのグリッド上で、全マスをちょうど1回ずつ通るループ（ハミルトン閉路）を作成する。
    
    Args:
        N (int): グリッドのサイズ (偶数であることを前提とする)
        
    Returns:
        list[tuple[int, int]]: ループの経路順の座標リスト
    """
    path = []
    
    # 0行目: (0,0)から(0, N-1)まで右に進む
    for c in range(N):
        path.append((0, c))
        
    # 1行目から(N-1)行目まで蛇行して進む
    for r in range(1, N):
        if r % 2 == 1:
            # 奇数行は右から左へ (c=N-1 から c=1 まで)
            # ※左端(c=0)は帰りのルートとして空けておく
            for c in range(N - 1, 0, -1):
                path.append((r, c))
        else:
            # 偶数行は左から右へ (c=1 から c=N-1 まで)
            for c in range(1, N):
                path.append((r, c))
                
    # 帰りのルート: 左端(c=0)を(N-1, 0)から(1, 0)まで上に戻る
    for r in range(N - 1, 0, -1):
        path.append((r, 0))
        
    return path


if __name__ == "__main__":
    main()