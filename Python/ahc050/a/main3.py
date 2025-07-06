# 差分評価可能な存在確率スコアを使ったP構築
# 既存の貪欲ベースのcalc()を改良

# グリッド内かどうかの判定
def in_grid(i,j):
    return 0 <= i < N and 0 <= j < N

# 各マス (i,j) が他のマスから滑り込む終点になる回数をスコア化
def compute_end_score(S):
    score = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if S[i][j] == "#":
                continue
            for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                ni,nj = i+dx,j+dy
                while in_grid(ni,nj) and S[ni][nj] != "#":
                    ni += dx
                    nj += dy
                # 壁手前のマスに滑ってくるなら、(ni-dx,nj-dy)が終点
                ni -= dx
                nj -= dy
                if in_grid(ni,nj) and S[ni][nj] != "#":
                    score[ni][nj] += 1
    return score

# 差分更新：壁を(x,y)に置いたとき、周囲に影響するマスのスコアを更新
def update_end_score(score, S, x, y):
    for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        ni,nj = x+dx,y+dy
        while in_grid(ni,nj) and S[ni][nj] != "#":
            # (ni,nj)から(x,y)に滑ってくる → (x,y)が壁になったので終点変更
            # (ni,nj)の滑り終点が(x,y)だったなら、その影響で別の終点になる
            old_end_i, old_end_j = ni, nj
            # 古い終点のスコアを下げる
            score[old_end_i][old_end_j] -= 1
            # 新しい壁により新しい終点
            nii,njj = ni+dx, nj+dy
            while in_grid(nii,njj) and S[nii][njj] != "#":
                nii += dx
                njj += dy
            nii -= dx
            njj -= dy
            if in_grid(nii,njj) and S[nii][njj] != "#":
                score[nii][njj] += 1
            ni += dx
            nj += dy

# スコアの低い順に岩を置くPを返す
def calc_dynamic(S):
    from heapq import heappush, heappop
    score = compute_end_score(S)
    used = [[False]*N for _ in range(N)]
    P = []

    for _ in range(N*N - M):
        # スコアの低い未使用マスを選ぶ
        candidates = []
        for i in range(N):
            for j in range(N):
                if S[i][j] != "#" and not used[i][j]:
                    heappush(candidates, (score[i][j], i, j))
        # 最も安全なマスに岩を置く
        _, x, y = heappop(candidates)
        P.append((x,y))
        used[x][y] = True
        S[x][y] = "#"
        update_end_score(score, S, x, y)

    return P

# 出力
def out(P):
    for i in P:
        print(f"{i[0]} {i[1]}")

# 入力
N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

# Pの構築
ans = calc_dynamic(S)
out(ans)
