#尺取り法
N ,K = map(int,input().split())
A = [int(x) for x in input().split()]
R = [0]*100009
B = [0]*100009
for i in range(N):
    B[i+1] = A[i]
#print(B)
for i in range(1,N):
    if i == 1:
        R[i] = 1
    else:
        R[i] = R[i-1]
    while R[i]<N and B[R[i]+1]-B[i] <= K:
        R[i] += 1

answer = 0
for i in range(1,N):
    answer += R[i]-i
print(answer)
