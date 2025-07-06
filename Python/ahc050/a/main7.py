# 焼きなまし法によるPの最適化（貪欲法を初期解として使用）

import time, math, random

# グリッド内かどうかの判定
def in_grid(i,j):
    return 0 <= i < N and 0 <= j < N

# 1ステップの拡散処理
def diffuse(prob, S):
    new_prob = [[0.0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if S[i][j] == "#" or prob[i][j] == 0.0:
                continue
            p = prob[i][j] / 4
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                ni, nj = i, j
                while in_grid(ni+dx, nj+dy) and S[ni+dx][nj+dy] != "#":
                    ni += dx
                    nj += dy
                new_prob[ni][nj] += p
    return new_prob

# Pに基づいてスコアを評価（期待生存ターン数）
def evaluate(P, S):
    prob = [[0.0]*N for _ in range(N)]
    total = sum(S[i][j] != '#' for i in range(N) for j in range(N))
    for i in range(N):
        for j in range(N):
            if S[i][j] != "#":
                prob[i][j] = 1 / total

    score = 0.0
    for x, y in P:
        score += sum(sum(row) for row in prob)  # 生存してる確率の合計が1なら +1
        prob[x][y] = 0.0  # 潰される確率消去
        S[x][y] = "#"
        prob = diffuse(prob, S)
    return score

# 焼きなましによるPの改善
def simulated_annealing(P_init, S_orig, time_limit=1.9):
    start = time.perf_counter()
    T0, T1 = 1.0, 0.01
    P = P_init[:]
    S_base = [row[:] for row in S_orig]
    best_score = evaluate(P, [row[:] for row in S_base])
    best_P = P[:]

    now_score = best_score
    while time.perf_counter() - start < time_limit:
        t = (time.perf_counter() - start) / time_limit
        T = T0 * (T1 / T0) ** t

        i, j = random.sample(range(len(P)), 2)
        P[i], P[j] = P[j], P[i]
        score = evaluate(P, [row[:] for row in S_base])

        if score > now_score or math.exp((score - now_score) / T) > random.random():
            now_score = score
            if score > best_score:
                best_score = score
                best_P = P[:]
        else:
            P[i], P[j] = P[j], P[i]  # rollback

    return best_P

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

# 初期解（貪欲）を使用
P0 = calc_prob_survival([row[:] for row in S])

# 焼きなまし
ans = simulated_annealing(P0, S)
out(ans)
