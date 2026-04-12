N = int(input())
A = [["" for _ in range(N)] for _ in range(N)]
A[0][(N-1)//2] = 1
prev = (0,(N-1)//2)
prev_num = 1
for i in range(N**2 - 1):
    if A[(prev[0]-1)%N][(prev[1]+1)%N] == "":
        A[(prev[0]-1)%N][(prev[1]+1)%N] = prev_num + 1
        prev = ((prev[0]-1)%N,(prev[1]+1)%N)
        prev_num += 1
    else:
        A[(prev[0]+1)%N][prev[1]] = prev_num + 1
        prev = ((prev[0]+1)%N,prev[1])
        prev_num += 1
for i in range(N):
    print(" ".join(map(str,A[i])))