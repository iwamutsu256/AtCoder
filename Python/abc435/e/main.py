import bisect

def merge_intervals(intervals, L, R):
    """
    黒く塗られた区間のリストを更新する関数
    intervals: [start1, end1, start2, end2, ...] の形式のリスト
    [L, R]: 新しく黒く塗る区間
    """
    if not intervals:
        return [L, R]

    # 新しい区間の始点Lがどの既存区間に含まれるか、またはどの区間の間にあるかを探す
    # bisect_leftは挿入点を返す。インデックスが偶数なら区間の外、奇数なら区間の中。
    left_idx = bisect.bisect_left(intervals, L)
    
    # 新しい区間の終点Rがどの既存区間に含まれるか、またはどの区間の間にあるかを探す
    right_idx = bisect.bisect_right(intervals, R)

    # 新しいマージ後の区間の始点を決定
    # left_idxが奇数なら、Lは既存の区間内。その区間の始点を新しい始点とする。
    if left_idx % 2 == 1:
        new_L = intervals[left_idx - 1]
    else:
        new_L = L

    # 新しいマージ後の区間の終点を決定
    # right_idxが奇数なら、Rは既存の区間内。その区間の終点を新しい終点とする。
    if right_idx % 2 == 1:
        new_R = intervals[right_idx]
    else:
        new_R = R

    # 新しい区間に完全に含まれる古い区間を削除し、新しい区間を挿入する
    # 始点側のスライスと終点側のスライスを結合し、間に新しい区間[new_L, new_R]を入れる
    merged_intervals = intervals[:left_idx] + [new_L, new_R] + intervals[right_idx:]
    
    # left_idxが奇数の場合、マージされて不要になった始点(intervals[left_idx-1])を削除
    if left_idx % 2 == 1:
        del merged_intervals[left_idx-1]
        
    return merged_intervals

N, Q = map(int, input().split())
# 黒く塗られた区間を [start1, end1, start2, end2, ...] の形式で保持する
black_intervals = []
total_black_cells = 0

for _ in range(Q):
    L, R = map(int, input().split())
    
    # 新しい区間をマージする前の黒マスの数を計算
    prev_black_cells = 0
    left_idx = bisect.bisect_right(black_intervals, L - 1)
    right_idx = bisect.bisect_left(black_intervals, R + 1)
    
    # [L,R]と重なる部分の既存区間の長さを計算
    temp_intervals = [L] + black_intervals[left_idx:right_idx] + [R]
    for i in range(0, len(temp_intervals) - 1, 2):
        s, e = temp_intervals[i], temp_intervals[i+1]
        prev_black_cells += (e - s + 1)

    # 区間リストを更新
    black_intervals = merge_intervals(black_intervals, L, R)
    
    # 更新後の黒マスの数を計算
    new_black_cells = 0
    left_idx = bisect.bisect_right(black_intervals, L - 1)
    right_idx = bisect.bisect_left(black_intervals, R + 1)
    
    # [L,R]と重なっていた部分がマージされた後の区間の長さを計算
    temp_intervals = black_intervals[left_idx:right_idx]
    for i in range(0, len(temp_intervals), 2):
        s, e = temp_intervals[i], temp_intervals[i+1]
        new_black_cells += (e - s + 1)
        
    # 黒マスの総数を差分更新
    total_black_cells += (new_black_cells - prev_black_cells)
    
    # 白いマスの数を出力
    print(N - total_black_cells)