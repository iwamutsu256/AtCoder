H,W = map(int,input().split())
Si,Sj = map(int,input().split())
C = [list(input()) for _ in range(H)]
X = list(input())
for i in range(len(X)):
    if X[i] == 'U':
        if 1 < Si and C[Si-2][Sj-1] != "#":
            Si -= 1
    elif X[i] == 'D':
        if Si < H and C[Si][Sj-1] != "#":
            Si += 1
    elif X[i] == 'L':
        if 1 < Sj and C[Si-1][Sj-2] != "#":
            Sj -= 1
    elif X[i] == 'R':
        if Sj < W and C[Si-1][Sj] != "#":
            Sj += 1
print(Si,Sj)