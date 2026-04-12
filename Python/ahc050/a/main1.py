# P計算
def calc(S):
    # 二重ループで岩が置かれていないものを前からPに代入
    P = []
    for i in range(N):
        for j in range(N):
            if S[i][j] != "#":
                P.append((i,j))
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