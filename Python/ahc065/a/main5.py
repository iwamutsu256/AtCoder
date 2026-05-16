import sys
import heapq
from collections import deque

def main():
    """
    メイン関数: 入力の受け取り、交差ネットワーク(縦横ループ)の構築、
    および「動的コスト付きダイクストラ法」を用いた高度なルーティングを実行する。
    """
    N = 20
    input() 
    
    grid = []
    for _ in range(N):
        grid.extend(list(map(int, input().split())))
        
    box_to_pos = [-1] * (N * N)
    for pos, box_id in enumerate(grid):
        box_to_pos[box_id] = pos
        
    # --- むつきの想定通り、盤面を「交差ネットワーク」に戻す ---
    conveyors = create_crossing_network(N)
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
    
    # 搬出口から各マスへの真の最短手数を事前計算
    min_dist_to_exit = precalculate_distances(EXIT_POS, cell_to_convs, conv_indices, N * N)
    
    if grid[EXIT_POS] == 0:
        grid[EXIT_POS] = -1
        start_target = 1
    else:
        start_target = 0
        
    all_operations = []
    
    # --- 全体ループ ---
    for target in range(start_target, N * N):
        
        # 動的コスト付きダイクストラ法で最適なルートを見つける
        best_path = dynamic_cost_dijkstra(
            box_to_pos, target, EXIT_POS, cell_to_convs, conv_indices, min_dist_to_exit
        )
        
        # 決定した操作列を適用
        for m, d in best_path:
            apply_action_inplace(grid, box_to_pos, m, d, conv_indices)
            all_operations.append((m, d))
            
        grid[EXIT_POS] = -1
        box_to_pos[target] = -1

    # 結果の出力
    print(len(all_operations))
    for m, d in all_operations:
        print(f"{m} {d}")


def create_crossing_network(N: int) -> list[list[tuple[int, int]]]:
    """
    NxNのグリッド上に、すべてのマスを網羅する縦横の交差ネットワーク(ループ)を作成する。
    1つのコンベアの長さは40であり、副作用(他の箱の移動)が非常に大きいのが特徴。
    """
    conveyors = []
    # 横方向ループ (10個)
    for k in range(N // 2):
        r1, r2 = 2 * k, 2 * k + 1
        loop = []
        for c in range(N):
            loop.append((r1, c))
        for c in range(N - 1, -1, -1):
            loop.append((r2, c))
        conveyors.append(loop)
        
    # 縦方向ループ (10個)
    for k in range(N // 2):
        c1, c2 = 2 * k, 2 * k + 1
        loop = []
        for r in range(N):
            loop.append((r, c1))
        for r in range(N - 1, -1, -1):
            loop.append((r, c2))
        conveyors.append(loop)
    return conveyors


def precalculate_distances(exit_pos: int, cell_to_convs: list[list[tuple[int, int]]], conv_indices: list[list[int]], total_cells: int) -> list[int]:
    """搬出口から各マスへの最短到達手数をBFSで事前計算する。"""
    dist = [9999] * total_cells
    dist[exit_pos] = 0
    queue = deque([exit_pos])
    while queue:
        curr = queue.popleft()
        for m, idx in cell_to_convs[curr]:
            L = len(conv_indices[m])
            for offset in (1, -1):
                nxt = conv_indices[m][(idx + offset) % L]
                if dist[nxt] == 9999:
                    dist[nxt] = dist[curr] + 1
                    queue.append(nxt)
    return dist


def dynamic_cost_dijkstra(b2p: list[int], target: int, exit_pos: int, cell_to_convs: list[list[tuple[int, int]]], conv_indices: list[list[int]], min_dist_to_exit: list[int]) -> list[tuple[int, int]]:
    """
    --- 貪欲法（高度化）の核心部: 動的コスト付きダイクストラ法 ---
    コンベアを動かす「コスト」を、未来の箱への影響に応じて動的に変化させる。
    交差ネットワークの巨大な副作用を利用し、未来の箱が近づくルートには「割引」を、
    遠ざかるルートには「ペナルティ」を与えて最短経路を探索する。
    """
    start_pos = b2p[target]
    if start_pos == exit_pos:
        return []
        
    # プライオリティキュー: (累積コスト, ターゲットの現在位置, 操作列)
    pq = [(0, 0, start_pos, [])]
    min_cost = {start_pos: 0}
    
    # 未来の箱に対する重み（長さ40のコンベアの副作用を強烈に評価する）
    future_weights = [80, 50, 20]
    
    while pq:
        curr_cost, _, curr_pos, path = heapq.heappop(pq)
        
        if curr_pos == exit_pos:
            return path
            
        if curr_cost > min_cost.get(curr_pos, float('inf')):
            continue
            
        for m, idx_in_conv in cell_to_convs[curr_pos]:
            L = len(conv_indices[m])
            
            for d, offset in [(1, 1), (-1, -1)]:
                nxt_pos = conv_indices[m][(idx_in_conv + offset) % L]
                
                # --- ダイクストラの核心部: 動的コスト計算 ---
                # 基本コストを100に設定 (割引でマイナスになるのを防ぐため)
                edge_cost = 100 
                
                # コンベアmを動かした時に、未来の箱(target+1 ~ +3)がどう動くかを評価
                for i in range(1, 4):
                    nxt_box = target + i
                    if nxt_box < 400:
                        box_pos = b2p[nxt_box]
                        # 未来の箱がこの巨大コンベアmに乗っている場合、巻き込まれて移動する
                        if box_pos != -1 and box_pos in conv_indices[m]:
                            box_idx_in_conv = conv_indices[m].index(box_pos)
                            new_box_pos = conv_indices[m][(box_idx_in_conv + offset) % L]
                            
                            # 搬出口までの距離の変化を計算
                            old_dist = min_dist_to_exit[box_pos]
                            new_dist = min_dist_to_exit[new_box_pos]
                            dist_diff = new_dist - old_dist # 遠ざかるとプラス、近づくとマイナス
                            
                            # 遠ざかるならコスト増、近づくならコスト減(割引)
                            edge_cost += future_weights[i-1] * dist_diff
                
                # どんなに割引されても最低コストは1とする
                edge_cost = max(1, edge_cost)
                
                nxt_cost = curr_cost + edge_cost
                
                if nxt_cost < min_cost.get(nxt_pos, float('inf')):
                    min_cost[nxt_pos] = nxt_cost
                    # tie-breakerとして path の長さを追加
                    heapq.heappush(pq, (nxt_cost, len(path) + 1, nxt_pos, path + [(m, d)]))
                    
    return []


def apply_action_inplace(grid: list[int], box_to_pos: list[int], m: int, d: int, conv_indices: list[list[int]]):
    """盤面を直接書き換える高速シミュレーション関数。"""
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