import bisect
N, Q = map(int,input().split())
masu = [0 for _ in range(N)]
left_count_index = dict()
index_left_count = dict()
for i in range(1,N+1):
    left_count_index[i] = i-1
for i in range(N):
    index_left_count[i] = i+1
min = 0
for _ in range(Q):
    query, xy = map(int,input().split())
    if query == 1:
        # 現在地と同じ数値の右端と交換
        current_num = masu[left_count_index[xy]]
        # rightとleftは左からX番目
        right = index_left_count[bisect.bisect_right(masu,current_num+1)-1]
        left = xy
        left_count_index[left],left_count_index[right] = left_count_index[right],left_count_index[left]
        index_left_count[left_count_index[left]] = left
        index_left_count[left_count_index[right]] = right
        masu[left_count_index[xy]] += 1
        min = masu[0]
    else:
        print(N-bisect.bisect_right(masu,xy+min-1))


