# インプット
n,m,k,t = map(int,input().split())
start = tuple(map(int,input().split()))
distinations = [tuple(map(int,input().split())) for _ in range(m)]

# 方針3
# 魔法陣をずっと使っていくとどんどん外側に寄っていき、効果的ではない
# 中心から外側に向かっていくときだけに限定してみる

cy, cx = start

magic_circles = []

for i in range(k):
    my,mx = 0,0
    if i == 0:
        my,mx = (cy+distinations[i][0])//2, (cx+distinations[i][1])//2
    else:
        my,mx = (distinations[i][0] + distinations[i+1][0])//2, (distinations[i][1]+distinations[i+1][1])//2
    print(my,mx)
    magic_circles.append((my,mx))

for i in range(len(distinations)):
    gy,gx = distinations[i]
    # ワープして早そうならワープする
    while True:
        path_length = abs(cy-gy)+abs(cx-gx)
        min_magic_circle = None
        mmc_num = None
        # すべての魔法陣に対して使った場合の最短距離を求める
        for j in range(k):
            mcy,mcx = magic_circles[j]
            temp_path_length = abs(gy-(2*mcy - cy)) + abs(gx-(2*mcx - cx)) + 1
            if path_length > temp_path_length and 0 <= (2*mcy - cy) < n and 0 <= (2*mcx - cx) < n and abs((n//2-0.5) - cx) < abs((n//2-0.5)-gx) and abs((n//2-0.5)-cy) < abs((n//2-0.5)-gy):
                min_magic_circle = (mcy,mcx)
                path_length = temp_path_length
                mmc_num = j
        # 短くならなかったら
        if min_magic_circle is None:
            break
        # 魔法陣実行
        mcy,mcx = min_magic_circle
        magic_circles[mmc_num] = (cy,cx)
        print("J",mcy,mcx)
        cy,cx = 2*mcy - cy, 2*mcx - cx
    for j in range(abs(gx-cx)):
        if gx > cx:
            print("R")
            cx += 1
        else:
            print("L")
            cx -= 1
    for j in range(abs(gy-cy)):
        if gy > cy:
            print("D")
            cy += 1
        else:
            print("U")
            cy -= 1