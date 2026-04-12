def rotate(S):
    new_S = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            new_S[i][j] = S[N-j-1][i]
    return new_S

N = int(input())
S = [list(input()) for _ in range(N)]
T = [list(input()) for _ in range(N)]
count_1 = 0
count_2 = 1
count_3 = 2
count_4 = 3
for i in range(N):
    for j in range(N):
        if S[i][j] != T[i][j]:
            count_1 += 1
S = rotate(S)
for i in range(N):
    for j in range(N):
        if S[i][j] != T[i][j]:
            count_2 += 1
S = rotate(S)
for i in range(N):
    for j in range(N):
        if S[i][j] != T[i][j]:
            count_3 += 1
S = rotate(S)
for i in range(N):
    for j in range(N):
        if S[i][j] != T[i][j]:
            count_4 += 1
print(min(count_1,count_2,count_3,count_4))