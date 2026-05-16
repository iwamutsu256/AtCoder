import sys
from collections import deque

def main():
    """
    メイン関数: 入力の受け取り、ハイブリッドネットワークの構築、
    および未来予測ビームサーチを用いたルーティングを実行する。
    """
    N = 20
    input() 
    
    grid = []
    for _ in range(N):
        grid.extend(list(map(int, input().split())))
        
    box_to_pos = [-1] * (N * N)
    for pos, box_id in enumerate(grid):
        box_to_pos[box_id] = pos
        
    # ハイブリッドネットワーク(2x2市松模様 + 外周ハイウェイ)の構築
    conveyors = create_hybrid_network(N)
    M = len(conveyors)
    
    # コンベア情報の出力
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
    
    EXIT_POS = 0 * N + (N // 2)  # (0, 10) -> 10
    
    # 各マスから搬出口への「真の最短手数」を事前計算 (評価関数で使用)
    min_dist_to_exit = precalculate_distances(EXIT_POS, cell_to_convs, conv_indices, N * N)
    
    if grid[EXIT_POS] == 0:
        grid[EXIT_POS] = -1
        start_target = 1
    else:
        start_target = 0
        
    all_operations = []
    
    # --- ビームサーチ: 全体ループ ---
    for target in range(start_target, N * N):
        # ビームサーチで「未来の箱への影響」も加味した最適な操作列を見つける
        best_path = beam_search_route(grid, box_to_pos, target, EXIT_POS, cell_to_convs, conv_indices, min_dist_to_exit)
        
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


def create_hybrid_network(N: int) -> list[list[tuple[int, int]]]:
    """
    NxNのグリッド上に、2x2の市松模様ループと外周環状線を作成する。
    """
    conveyors = []
    for r in range(0, N, 2):
        for c in range(0, N, 2):
            conveyors.append([(r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c)])
            
    for r in range(1, N - 1, 2):
        for c in range(1, N - 1, 2):
            conveyors.append([(r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c)])
            
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


def precalculate_distances(exit_pos: int, cell_to_convs: list[list[tuple[int, int]]], conv_indices: list[list[int]], total_cells: int) -> list[int]:
    """
    搬出口(exit_pos)から各マスへの最短到達手数をBFSで事前計算する。
    これにより、評価関数内で正確な距離をO(1)で参照できる。
    """
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


def evaluate_state(b2p: list[int], target: int, path_len: int, target_pos: int, min_dist_to_exit: list[int]) -> int:
    """
    --- ビームサーチの核心部: 評価関数 ---
    現在の状態の良さをスコア化する(値が小さいほど優秀)。
    ターゲットの距離、消費ターン数に加え、未来の箱への影響を強く評価する。
    """
    # 1. 主目的: ターゲット箱の搬出口への真の距離 (最優先するため重み大)
    score = min_dist_to_exit[target_pos] * 10000
    
    # 2. ターン数のペナルティ
    score += path_len * 1000
    
    # 3. 未来予測: 次の箱〜その3つ先までの箱が搬出口に近いほど高評価
    weights = [80, 40, 20, 10]
    for i in range(1, 5):
        nxt_box = target + i
        if nxt_box < 400:
            pos = b2p[nxt_box]
            if pos != -1:
                score += min_dist_to_exit[pos] * weights[i - 1]
                
    return score


def beam_search_route(start_grid: list[int], start_b2p: list[int], target: int, exit_pos: int, cell_to_convs: list[list[tuple[int, int]]], conv_indices: list[list[int]], min_dist_to_exit: list[int]) -> list[tuple[int, int]]:
    """
    --- ビームサーチの核心部: 状態探索 ---
    未来の箱を考慮しながら、ターゲット箱を搬出口に運ぶ最適な手順を探索する。
    """
    start_pos = start_b2p[target]
    if start_pos == exit_pos:
        return []
        
    BEAM_WIDTH = 10
    MAX_DEPTH = 50
    
    # beam要素: (評価スコア, grid, box_to_pos, path, 現在のターゲット位置)
    initial_score = evaluate_state(start_b2p, target, 0, start_pos, min_dist_to_exit)
    beam = [(initial_score, start_grid[:], start_b2p[:], [], start_pos)]
    
    best_goal_path = []
    best_goal_score = float('inf')
    
    for depth in range(MAX_DEPTH):
        next_states = []
        seen_hashes = set()
        
        for score, g, b2p, path, curr_pos in beam:
            # ゴールに到達した状態はキープし、より良いものがあれば更新
            if curr_pos == exit_pos:
                if score < best_goal_score:
                    best_goal_score = score
                    best_goal_path = path
                continue
                
            # ターゲット箱が乗っているコンベア(最大2つ)だけを回して枝分かれを作る
            for m, idx_in_conv in cell_to_convs[curr_pos]:
                for d in (1, -1):
                    new_g = g[:]
                    new_b2p = b2p[:]
                    
                    apply_action_inplace(new_g, new_b2p, m, d, conv_indices)
                    new_path = path + [(m, d)]
                    new_pos = new_b2p[target]
                    
                    # 状態の重複排除 (盤面のハッシュ値を利用)
                    state_hash = hash(tuple(new_g))
                    if state_hash not in seen_hashes:
                        seen_hashes.add(state_hash)
                        
                        new_score = evaluate_state(new_b2p, target, len(new_path), new_pos, min_dist_to_exit)
                        next_states.append((new_score, new_g, new_b2p, new_path, new_pos))
                        
        if not next_states and best_goal_score != float('inf'):
            break
            
        # --- ビームサーチの核心部: 上位K個の状態を選択 ---
        next_states.sort(key=lambda x: x[0])
        beam = next_states[:BEAM_WIDTH]
        
    return best_goal_path


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