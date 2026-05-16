import sys
from collections import deque

def main():
    """
    メイン関数: 入力の受け取り、交差ネットワークコンベアの構築、
    およびBFSを用いた単一箱の貪欲ルーティングを実行する。
    """
    # Nは20で固定
    N = 20
    # 標準入力からNを読み飛ばす（すでに20と分かっているが、入力フォーマットに合わせる）
    input() 
    
    # a: 倉庫の初期状態 (1次元配列として保持)
    grid = []
    for _ in range(N):
        grid.extend(list(map(int, input().split())))
        
    # コンベアネットワークの構築 (横10個、縦10個の計20個)
    conveyors = create_crossing_network(N)
    M = len(conveyors)
    
    # コンベアの出力情報の構築
    print(M)
    for loop in conveyors:
        conveyor_out = [len(loop)]
        for r, c in loop:
            conveyor_out.extend([r, c])
        print(*conveyor_out)
    
    # 各コンベアの座標を1次元インデックス(0~399)に変換しておく
    conv_indices = []
    for loop in conveyors:
        indices = [r * N + c for r, c in loop]
        conv_indices.append(indices)
        
    # 高速なBFSのために、各マスが「どのコンベアの」「どのインデックスにあるか」を事前計算
    cell_to_convs = [[] for _ in range(N * N)]
    for m, conv in enumerate(conv_indices):
        for idx_in_conv, pos in enumerate(conv):
            cell_to_convs[pos].append((m, idx_in_conv))
    
    # 搬出口の1次元インデックス
    EXIT_POS = 0 * N + (N // 2)  # 10
    
    # 初期状態で箱0が搬出口にある場合は、操作前に取り除かれる
    if grid[EXIT_POS] == 0:
        grid[EXIT_POS] = -1 # -1 は空きマスを表す
        start_target = 1
    else:
        start_target = 0
        
    all_operations = []
    
    # --- 貪欲法の全体ループ ---
    # 箱を0から順番に搬出していく
    for target in range(start_target, N * N):
        # 1. ターゲットの箱の現在位置を探す
        start_pos = grid.index(target)
        
        # 2. BFSでターゲットを搬出口に運ぶための最短操作列を見つける
        ops = bfs_shortest_path(start_pos, EXIT_POS, cell_to_convs, conv_indices)
        
        # 3. 見つけた操作列を実際のグリッドに適用する
        for m, d in ops:
            grid = apply_action(grid, m, d, conv_indices)
            all_operations.append((m, d))
            
        # 4. ターゲットが搬出口に到達したので、取り除かれる（空きマスになる）
        grid[EXIT_POS] = -1

    # 操作結果の出力
    print(len(all_operations))
    for m, d in all_operations:
        print(f"{m} {d}")


def create_crossing_network(N: int) -> list[list[tuple[int, int]]]:
    """
    NxNのグリッド上に、すべてのマスを網羅する縦横の交差ネットワーク(ループ)を作成する。
    各マスはちょうど1つの横ループと1つの縦ループに属する。
    
    Args:
        N (int): グリッドのサイズ (20)
        
    Returns:
        list[list[tuple[int, int]]]: コンベアの経路(座標リスト)のリスト
    """
    conveyors = []
    
    # 横方向のループ (2行で1つのループを形成、合計10ループ)
    for k in range(N // 2):
        r1, r2 = 2 * k, 2 * k + 1
        loop = []
        for c in range(N):
            loop.append((r1, c))
        for c in range(N - 1, -1, -1):
            loop.append((r2, c))
        conveyors.append(loop)
        
    # 縦方向のループ (2列で1つのループを形成、合計10ループ)
    for k in range(N // 2):
        c1, c2 = 2 * k, 2 * k + 1
        loop = []
        for r in range(N):
            loop.append((r, c1))
        for r in range(N - 1, -1, -1):
            loop.append((r, c2))
        conveyors.append(loop)
        
    return conveyors


def bfs_shortest_path(start_pos: int, target_pos: int, cell_to_convs: list[list[tuple[int, int]]], conv_indices: list[list[int]]) -> list[tuple[int, int]]:
    """
    ターゲットとなる箱１つだけに注目し、現在位置から目標位置までの最短のコンベア操作列を探索する。
    
    Args:
        start_pos (int): 箱の現在位置 (1次元インデックス)
        target_pos (int): 目標位置 (搬出口の1次元インデックス)
        cell_to_convs (list): 各マスが属するコンベアIDとその中でのインデックスのリスト
        conv_indices (list): コンベアごとのマスのリスト
        
    Returns:
        list[tuple[int, int]]: 最短で目標に到達するための操作列 [(コンベアID, 方向), ...]
    """
    # 既に目標位置にいる場合は操作不要
    if start_pos == target_pos:
        return []
        
    # --- 貪欲法の核心部: 単一箱の最短経路探索 (BFS) ---
    # queueには (現在位置, ここまでの操作列) を格納する
    queue = deque([(start_pos, [])])
    visited = {start_pos}
    
    while queue:
        curr_pos, path = queue.popleft()
        
        # 現在位置が属している最大2つのコンベアについて、動かした先の位置を調べる
        for m, idx_in_conv in cell_to_convs[curr_pos]:
            L = len(conv_indices[m])
            
            # 操作1: コンベアを正方向(d=1)に回した場合
            # 箱はコンベア上の次のインデックスに移動する
            nxt_pos_1 = conv_indices[m][(idx_in_conv + 1) % L]
            if nxt_pos_1 not in visited:
                if nxt_pos_1 == target_pos:
                    return path + [(m, 1)]
                visited.add(nxt_pos_1)
                queue.append((nxt_pos_1, path + [(m, 1)]))
                
            # 操作2: コンベアを逆方向(d=-1)に回した場合
            # 箱はコンベア上の前のインデックスに移動する
            nxt_pos_m1 = conv_indices[m][(idx_in_conv - 1) % L]
            if nxt_pos_m1 not in visited:
                if nxt_pos_m1 == target_pos:
                    return path + [(m, -1)]
                visited.add(nxt_pos_m1)
                queue.append((nxt_pos_m1, path + [(m, -1)]))
                
    return []


def apply_action(grid: list[int], m: int, d: int, conv_indices: list[list[int]]) -> list[int]:
    """
    指定したコンベアを動かし、盤面上のすべての箱（および空きマス）を移動させる。
    ※この処理はシミュレーション用（実際の操作適用）であり、BFSの探索中には呼ばれないため高速。
    
    Args:
        grid (list[int]): 現在のグリッド(1次元配列)
        m (int): 動かすコンベアの番号
        d (int): 動かす方向 (1 または -1)
        conv_indices (list[list[int]]): 各コンベアが通る1次元インデックスのリスト
        
    Returns:
        list[int]: 操作後の新しいグリッド
    """
    new_grid = grid[:]
    indices = conv_indices[m]
    L = len(indices)
    
    if d == 1:
        # 正方向への循環シフト
        tmp = new_grid[indices[-1]]
        for i in range(L - 1, 0, -1):
            new_grid[indices[i]] = new_grid[indices[i - 1]]
        new_grid[indices[0]] = tmp
    else:
        # 逆方向への循環シフト
        tmp = new_grid[indices[0]]
        for i in range(L - 1):
            new_grid[indices[i]] = new_grid[indices[i + 1]]
        new_grid[indices[-1]] = tmp
        
    return new_grid


if __name__ == "__main__":
    main()