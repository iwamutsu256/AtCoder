N, M = map(int,input().split())
L = [0] * N
for i in range(M):
    A,B = map(int,input().split())
    L[A-1] += 1
    L[B-1] += 1
for i in range(N-1):
    print((N-L[i]-1)*(N-L[i]-2)*(N-L[i]-3)//6,end=" ")
print((N-L[N-1]-1)*(N-L[N-1]-2)*(N-L[N-1]-3)//6)