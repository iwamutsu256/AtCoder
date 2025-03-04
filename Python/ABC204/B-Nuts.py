N = int(input())
A = [int(x) for x in input().split()]
count = 0
for i in range(N):
    if A[i] > 10:
        count += A[i] - 10
print(count)