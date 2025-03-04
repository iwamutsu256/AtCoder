N,K = map(int,input().split())
A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
count = 0
for i in range(N):
    count += abs(A[i] - B[i])
if K >= count and (K-count)%2 == 0:
    print("Yes")
else:
    print("No")