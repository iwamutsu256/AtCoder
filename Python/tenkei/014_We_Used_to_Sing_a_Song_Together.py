N = int(input())
A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
A.sort()
B.sort()
count = 0
for i in range(N):
    count += abs(A[i]-B[i])
print(count)