N = int(input())
A = [int(x) for x in input().split()]
for i in range(N):
    if A[i] % 2 == 0:
        print(A[i],end=" ")
print()