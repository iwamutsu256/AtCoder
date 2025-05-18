N,M,L = map(int,input().split())
S = ["" for _ in range(N)]
P = [0 for _ in range(N)]
# S,Pを配列に保存 
for i in range(N):
    S[i],P[i] = input().split()
    S[i] = list(S[i])
    P[i] = int(P[i])
# アルファベットごとの出現率のリストを作成
# 次の文字とその重みを保存
dic = {"a":[],"b":[],"c":[],"d":[],"e":[],"f":[]}
Q = sorted(P,reverse=True)
# 重みが上位5個を厳選
Q = Q[:3]
for i in range(N):
    for j in range(len(S[i])-1):
        # 次の文字とその重みのリスト
        dic[S[i][j]].append([S[i][j+1],P[i]])
# print(dic)
# 状態を6個とした遷移行列を作成
A = []
for alpha in dic.keys():
    B = [0,0,0,0,0,0]
    C = dic[alpha]
    # 重みの合計を計算
    sam = 0
    for i in range(len(C)):
        if C[i][1] in Q:
            sam += C[i][1]**2
    # それぞれの要素に確率をfloatで保存
    for i in range(len(C)):
        if C[i][1] in Q:
            B[ord(C[i][0])-97] += C[i][1]**2/sam
    # 全部を足したら100になるように調整
    for i in range(len(B)-1):
        B[i] = int(B[i]*100)
    B[5] = 100 - sum(B[:5])
    A.append(B)
# print(A)
# 前半の状態のみで実行する
# 後半は自己ループのみにして、使わない
for i in range(6):
    print(chr(97+i)," ".join(map(str,A[i]+[0,0,0,0,0,0])))
for i in range(6):
    D = [0 for _ in range(12)]
    D[6+i] = 100
    print(chr(97+i), " ".join(map(str,D)))