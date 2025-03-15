N = int(input())
S = []
maximum = 0
for i in range(N):
    S.append(list(input()))
    maximum = max(maximum, len(S[i]))
T = [["*" for _ in range(N)] for _ in range(maximum)]
flag = [False for _ in range(maximum)]
for i in range(N):
    for j in range(maximum):
        if len(S[i]) <= j and flag[j] == False:
            T[j][N-1-i] = ""
        elif len(S[i]) <= j:
            pass
        else:
            T[j][N-1-i] = S[i][j]
            flag[j] = True
for i in range(maximum):
    print("".join(T[i]))