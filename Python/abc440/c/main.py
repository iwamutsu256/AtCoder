# 累積和を作る　O(N)
# 1回のコスト計算　O(N/W)
# 必要なコスト計算回数 O(W)
# コスト計算 O(N)

# あまりで和を分類

T = int(input())
for _ in range(T):
    N,W = map(int,input().split())
    C = list(map(int,input().split()))
    # Cのあまり分類配列
    C_sum = [0] * 2*W
    for i in range(N):
        C_sum[i%(2*W)] += C[i]
    C_sum = C_sum + C_sum[:W]
    # print(C_sum)
    count = sum(C_sum[:W])
    mini = count
    for j in range(2*W):
        count += C_sum[j+W-1] - C_sum[j-1]
        mini = min(mini,count)
        # print(count)
    print(mini)