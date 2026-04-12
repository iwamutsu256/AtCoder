N,M,L = map(int,input().split())
favo = 0
favo_S = ""

# 一番favoriteな文字列を探す
for i in range(N):
    S,P = input().split()
    P = int(P)
    if P >= favo:
        favo = P
        favo_S = S
# 文字列を1文字ずつのリストに変換
favo_S = list(favo_S)
# 12文字以下の場合、末尾にAを追加
while len(favo_S) < 12:
    favo_S.append("a")

# １文字ずつ次の状態に遷移していく
for i in range(12):
    # １行ごとの遷移行列をTとする
    T = [0 for _ in range(12)]
    T[(i+1)%12] = 100
    print(favo_S[i], " ".join(map(str,T)))