N,K = map(int,input().split())
A = [int(x) for x in input().split()]
for i in range(N):
    if A[i] % K == 0:
        print(A[i]//K,end=" ")
print()