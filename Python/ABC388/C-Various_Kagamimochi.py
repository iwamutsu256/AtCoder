N = int(input())
A = [int(x) for x in input().split()]
B = [0]*1000000
R = [0]*1000000
for i in range(1,N+1):
    B[i] = A[i-1]
for i in range(1,N):
    if i == 1:
        R[i] = 1
    else:
        R[i] = R[i-1]
    while R[i] < N and B[R[i]+1]/B[i] < 2.0:
        R[i] += 1
ans = 0
for i in range(1,N):
    ans += R[i] - i
    #print(R[i])
print((N**2-N)//2-ans)