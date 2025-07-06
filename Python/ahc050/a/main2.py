# グリッドないかどうか
def in_grid(i,j):
    if 0 <= i <= N-1 and 0 <= j <= N-1:
        return True
    else:
        return False

# P計算
def calc(S):
    # 二重ループで各マスの周囲の開いているマスを確認
    # その個数の少ない（安全）順にソートし、Pに追加
    P = []
    Q = []
    for i in range(N):
        for j in range(N):
            if S[i][j] != "#":
                score = 0
                for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    ni,nj = i,j
                    while in_grid(ni+dx, nj+dy) and S[ni+dx][nj+dy] != "#":
                        ni += dx
                        nj += dy
                        score += 1
                Q.append((score,i,j))
    Q.sort()
    for i in Q:
        P.append((i[1],i[2]))
    return P

# 出力
def out(P):
    for i in P:
        print(f"{i[0]} {i[1]}")

# 入力を受け取る
N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]
ans = calc(S)
out(ans)