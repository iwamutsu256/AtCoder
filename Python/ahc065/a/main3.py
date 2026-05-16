import sys
from collections import deque

def main():
    """
    メイン関数: 入力の受け取り、ハイブリッドネットワーク(2x2市松模様+外周環状線)の構築、
    およびBFSを用いた高速貪欲ルーティングを実行する。
    """
    N = 20
    input() 
    
    grid = []
    for _ in range(N):
        grid.extend(list(map(int, input().split())))
        
    box_to_pos = [-1] * (N * N)
    for pos, box_id in enumerate(grid):
        box_to_pos[box_id] = pos
        
    # --- むつきのアイデア: ハイブリッドネットワークの構築 ---
    conveyors = create_hybrid_network(N)
    M = len(conveyors)
    
    print(M)
    for loop in conveyors:
        conveyor_out = [len(loop)]
        for r, c in loop:
            conveyor_out.extend([r, c])
        print(*conveyor_out)
    
    conv_indices = []
    for loop in conveyors:
        indices = [r * N + c for r, c in loop]
        conv_indices.append(indices)
        
    cell_to_convs = [[] for _ in range(N * N)]
    for m, conv in enumerate(conv_indices):
        for idx_in_conv, pos in enumerate(conv):
            cell_to_convs[pos].append((m, idx_in_conv))
    
    EXIT_POS = 0 * N + (N // 2)  # 10
    
    if grid[EXIT_POS] == 0:
        grid[EXIT_POS] = -1
        start_target = 1
    else:
        start_target = 0
        
    all_operations = []
    
    # --- 貪欲法: 箱を順番に搬出 ---
    for target in range(start_target, N * N):
        start_pos = box_to_pos[target]
        
        # 最短経路を探索（ハイウェイも自動的に経路の候補に入る）
        ops = bfs_shortest_path(start_pos, EXIT_POS, cell_to_convs, conv_indices)
        
        for m, d in ops:
            apply_action_inplace(grid, box_to_pos, m, d, conv_indices)
            all_operations.append((m, d))
            
        grid[EXIT_POS] = -1
        box_to_pos[target] = -1

    print(len(all_operations))
    for m, d in all_operations:
        print(f"{m} {d}")


def create_hybrid_network(N: int) -> list[list[tuple[int, int]]]:
    """
    NxNのグリッド上に、2x2の市松模様ループと、外周を囲む巨大なハイウェイループを作成する。
    
    Args:
        N (int): グリッドのサイズ (20)
        
    Returns:
        list[list[tuple[int, int]]]: 合計182個のコンベアネットワーク
    """
    conveyors = []
    
    # 1. グループA: (偶数, 偶数) の2x2ループ (100個)
    for r in range(0, N, 2):
        for c in range(0, N, 2):
            conveyors.append([(r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c)])
            
    # 2. グループB: (奇数, 奇数) の2x2ループ (81個)
    for r in range(1, N - 1, 2):
        for c in range(1, N - 1, 2):
            conveyors.append([(r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c)])
            
    # 3. 外周ハイウェイ (1個): 盤面の一番外側を時計回りに一周する
    highway = []
    for c in range(N):
        highway.append((0, c))
    for r in range(1, N - 1):
        highway.append((r, N - 1))
    for c in range(N - 1, -1, -1):
        highway.append((N - 1, c))
    for r in range(N - 2, 0, -1):
        highway.append((r, 0))
        
    conveyors.append(highway)
            
    return conveyors


def bfs_shortest_path(start_pos: int, target_pos: int, cell_to_convs: list[list[tuple[int, int]]], conv_indices: list[list[int]]) -> list[tuple[int, int]]:
    """
    --- 貪欲法の核心部: ルーティング探索 ---
    ローカル線(2x2)とハイウェイを区別せず、目的の箱を搬出口へ運ぶ最短手数を探索する。
    """
    if start_pos == target_pos:
        return []
        
    queue = deque([(start_pos, [])])
    visited = {start_pos}
    
    while queue:
        curr_pos, path = queue.popleft()
        
        for m, idx_in_conv in cell_to_convs[curr_pos]:
            L = len(conv_indices[m]) # 長さ4 または 長さ76 に動的に対応
            
            for d, offset in [(1, 1), (-1, -1)]:
                nxt_pos = conv_indices[m][(idx_in_conv + offset) % L]
                if nxt_pos not in visited:
                    if nxt_pos == target_pos:
                        return path + [(m, d)]
                    visited.add(nxt_pos)
                    queue.append((nxt_pos, path + [(m, d)]))
                
    return []


def apply_action_inplace(grid: list[int], box_to_pos: list[int], m: int, d: int, conv_indices: list[list[int]]):
    """
    盤面を直接書き換える高速シミュレーション関数。
    """
    indices = conv_indices[m]
    L = len(indices)
    
    if d == 1:
        tmp_val = grid[indices[-1]]
        for i in range(L - 1, 0, -1):
            val = grid[indices[i - 1]]
            grid[indices[i]] = val
            if val != -1:
                box_to_pos[val] = indices[i]
        grid[indices[0]] = tmp_val
        if tmp_val != -1:
            box_to_pos[tmp_val] = indices[0]
    else:
        tmp_val = grid[indices[0]]
        for i in range(L - 1):
            val = grid[indices[i + 1]]
            grid[indices[i]] = val
            if val != -1:
                box_to_pos[val] = indices[i]
        grid[indices[-1]] = tmp_val
        if tmp_val != -1:
            box_to_pos[tmp_val] = indices[-1]

if __name__ == "__main__":
    main()