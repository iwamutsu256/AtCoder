N,M = map(int,input().split())
A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
ans = 0
for i in range(M):
    ans += A[B[i]-1]
print(ans)