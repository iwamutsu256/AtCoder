# 確率拡散（継続的）に基づくP構築（生存確率追跡型）

# グリッド内かどうかの判定
def in_grid(i,j):
    return 0 <= i < N and 0 <= j < N

# 拡散処理（1ステップ分）：現時点のprobを受け取り、次の分布を返す
def diffuse(prob, S):
    new_prob = [[0.0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if S[i][j] == "#": continue
            if prob[i][j] == 0.0: continue
            p = prob[i][j] / 4
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                ni, nj = i, j
                while in_grid(ni+dx, nj+dy) and S[ni+dx][nj+dy] != "#":
                    ni += dx
                    nj += dy
                new_prob[ni][nj] += p
    return new_prob

# 拡散確率に基づいて岩を置く（状態を保持しながら確率を更新）
def calc_prob_survival(S):
    from heapq import heappush, heappop
    used = [[False]*N for _ in range(N)]
    P = []

    total_steps = N*N - M
    prob = [[0.0]*N for _ in range(N)]
    total = sum(S[i][j] != '#' for i in range(N) for j in range(N))
    for i in range(N):
        for j in range(N):
            if S[i][j] != "#":
                prob[i][j] = 1 / total

    for turn in range(total_steps):
        candidates = []
        for i in range(N):
            for j in range(N):
                if S[i][j] != "#" and not used[i][j]:
                    heappush(candidates, (prob[i][j], i, j))
        _, x, y = heappop(candidates)
        P.append((x,y))
        used[x][y] = True
        S[x][y] = "#"  # 壁を置く

        # ロボットが潰された確率を削除
        prob[x][y] = 0.0
        # 残りの確率を1ステップ拡散
        prob = diffuse(prob, S)

    return P

# 出力
def out(P):
    for i in P:
        print(f"{i[0]} {i[1]}")

# 入力
N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

# Pの構築
ans = calc_prob_survival(S)
out(ans)
