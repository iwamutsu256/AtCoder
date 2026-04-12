# 確率拡散に基づくP構築（貪欲法改良版）

# グリッド内かどうかの判定
def in_grid(i,j):
    return 0 <= i < N and 0 <= j < N

# ロボットが存在する確率分布をステップごとに拡散で計算
def compute_prob_map(S, steps=3):
    total = sum(S[i][j] != '#' for i in range(N) for j in range(N))
    prob = [[0.0]*N for _ in range(N)]

    # 初期確率：全空きマスに均等配置
    for i in range(N):
        for j in range(N):
            if S[i][j] != "#":
                prob[i][j] = 1 / total

    for _ in range(steps):
        new_prob = [[0.0]*N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if S[i][j] == "#": continue
                p = prob[i][j] / 4
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    ni, nj = i, j
                    while in_grid(ni+dx, nj+dy) and S[ni+dx][nj+dy] != "#":
                        ni += dx
                        nj += dy
                    new_prob[ni][nj] += p
        prob = new_prob

    return prob

# 確率に基づいて安全な順に岩を置くPを構築（600ターン目以降は静的な評価）
def calc_prob_based(S):
    from heapq import heappush, heappop
    used = [[False]*N for _ in range(N)]
    P = []

    total_steps = N*N - M
    threshold = 600  # 拡散確率計算を行うターン数の上限

    for turn in range(total_steps):
        if turn < threshold:
            prob = compute_prob_map(S, steps=3)
        else:
            # 以降は静的な degree ベースの簡易評価
            prob = [[0.0]*N for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    if S[i][j] == "#": continue
                    score = 0
                    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                        ni, nj = i, j
                        while in_grid(ni+dx, nj+dy) and S[ni+dx][nj+dy] != "#":
                            ni += dx
                            nj += dy
                            score += 1
                    prob[i][j] = score

        candidates = []
        for i in range(N):
            for j in range(N):
                if S[i][j] != "#" and not used[i][j]:
                    heappush(candidates, (prob[i][j], i, j))
        _, x, y = heappop(candidates)
        P.append((x,y))
        used[x][y] = True
        S[x][y] = "#"  # 壁を置く

    return P

# 出力
def out(P):
    for i in P:
        print(f"{i[0]} {i[1]}")

# 入力
N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

# Pの構築
ans = calc_prob_based(S)
out(ans)
