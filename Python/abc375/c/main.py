def minimum_dist(i,j):
    x = min(i+1,N-i)
    y = min(j+1,N-j)
    return min(x,y)

def p_ans(A):
    for i in range(N):
        print("".join(A[i]))

N = int(input())
A = [list(input()) for _ in range(N)]
B = [["?" for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if minimum_dist(i,j) % 4 == 1:
            B[j][N-i-1] = A[i][j]
        elif minimum_dist(i,j) % 4 == 2:
            B[N-i-1][N-j-1] = A[i][j]
        elif minimum_dist(i,j) % 4 == 3:
            B[N-j-1][i] = A[i][j]
        else:
            B[i][j] = A[i][j]
p_ans(B)

