N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]
T = [list(input()) for _ in range(M)]
for i in range(N-M+1):
    for j in range(N-M+1):
        flag = True
        for k in range(M):
            for l in range(M):
                if S[i+k][j+l] != T[k][l]:
                    flag = False
        if flag:
            print(i+1,j+1)