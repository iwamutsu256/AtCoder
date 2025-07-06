# 焼きなまし法によるPの最適化（差分評価・複数近傍対応・デバッグ付き）

import time, math, random, sys

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

# 与えられた区間でスコアを計算（差分評価用）
def evaluate_partial(P, S, prob, begin):
    score = 0.0
    for turn in range(begin, len(P)):
        x, y = P[turn]
        total_prob = sum(sum(row) for row in prob)
        score += total_prob
        #if turn % 100 == 0:
        #    print(f"[DEBUG] turn={turn}, total_prob={total_prob:.6f}", file=sys.stderr)
        prob[x][y] = 0.0
        S[x][y] = "#"
        prob = diffuse(prob, S)
    return score, prob

# 焼きなましによるPの改善（複数近傍 + 差分評価）
def simulated_annealing(P_init, S_orig, time_limit=1.4):
    start = time.perf_counter()
    T0, T1 = 1.0, 0.01
    P = P_init[:]
    S_base = [row[:] for row in S_orig]
    n = len(P)

    # 初期状態のスコアと拡散状態をすべて保存
    total = sum(S_base[i][j] != '#' for i in range(N) for j in range(N))
    prob = [[1 / total if S_base[i][j] != '#' else 0.0 for j in range(N)] for i in range(N)]
    prob_states = []
    s = [row[:] for row in S_base]
    score_prefix = []
    score = 0.0
    for turn in range(n):
        x, y = P[turn]
        total_prob = sum(sum(row) for row in prob)
        score += total_prob
        score_prefix.append(score)
        prob_states.append((s, prob))
        prob[x][y] = 0.0
        s = [row[:] for row in s]
        s[x][y] = "#"
        prob = diffuse(prob, s)

    best_score = score
    best_P = P[:]
    now_score = score

    while time.perf_counter() - start < time_limit:
        t = (time.perf_counter() - start) / time_limit
        T = T0 * (T1 / T0) ** t

        move_type = random.randint(0, 2)
        if move_type == 0:
            # swap 2点
            i, j = random.sample(range(n), 2)
            P[i], P[j] = P[j], P[i]
            modified = [i, j]
        elif move_type == 1:
            # 範囲逆転
            i, j = sorted(random.sample(range(n), 2))
            P[i:j+1] = reversed(P[i:j+1])
            modified = list(range(i, j+1))
        else:
            # 1点を別の場所に移動
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
            if i < j:
                P = P[:i] + P[i+1:j+1] + [P[i]] + P[j+1:]
                modified = list(range(i, j+1))
            elif i > j:
                P = P[:j] + [P[i]] + P[j:i] + P[i+1:]
                modified = list(range(j, i+1))
            else:
                continue

        i = min(modified)
        s_copy = [row[:] for row in prob_states[i][0]]
        p_copy = [row[:] for row in prob_states[i][1]]
        delta_score, _ = evaluate_partial(P, s_copy, p_copy, i)
        new_score = (score_prefix[i-1] if i > 0 else 0.0) + delta_score

        if new_score > now_score or math.exp((new_score - now_score) / T) > random.random():
            now_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_P = P[:]
                print(f"[INFO] New best score: {best_score:.6f} at t={t:.2f}", file=sys.stderr)
        else:
            # rollback
            P = P_init[:]

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
