import copy
S = [list(input()) for i in range(8)]
T = copy.deepcopy(S)
U = copy.deepcopy(S)
#縦についてみる
for i in range(8):
    for j in range(8):
        if S[j][i] == "#":
            for k in range(8):
                T[k][i] = "#"
            else:
                break
#横についてみる
for i in range(8):
    for j in range(8):
        if S[i][j] == "#":
            for k in range(8):
                U[i][k] = "#"
            else:
                break
sum = 0
for i in range(8):
    for j in range(8):
        if T[i][j] == "." and U[i][j] == ".":
            sum += 1
print(sum)