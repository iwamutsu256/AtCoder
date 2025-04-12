N,K = map(int,input().split())
S = list(input())
max_o = 0
for i in range(N):
    # ?の両隣のどちらかがoなら.にする
    if S[i] == "?" and ((i < N-1 and S[i+1] == "o") or (i > 0 and S[i-1] == "o")):
        S[i] = "."
q = []
o_count = 0
for i in range(N):
    # 新しく?が始まったら
    if S[i] == "?" and (i == 0 or S[i-1] != "?"):
        start = i
    if S[i] == "?" and (i == N-1 or S[i+1] != "?"):
        end = i
        # ?の長さ
        length = end - start + 1
        q.append(length)
        # oを含むことができる最大数
        if length % 2 == 0:
            max_o += length // 2
        else:
            max_o += length // 2 + 1 
    if S[i] == "o":
        o_count += 1
if max_o > K-o_count:
    print("".join(S))
elif K-o_count == 0:
    for i in range(N):
        if S[i] == "?":
            S[i] = "."
    print("".join(S))
else:
    count = 0
    for i in range(N):
        if S[i] == "?":
            if q[count] % 2 == 0:
                if i < N-1 and S[i+1] != "?":
                    count += 1
            else:
                for j in range(q[count]):
                    if j % 2 == 0:
                        S[i+j] = "o"
                    else:
                        S[i+j] = "."
                count += 1
    print("".join(S))