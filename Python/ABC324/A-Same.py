N = int(input())
A = [int(x) for x in input().split()]
if A.count(A[0]) == N:
    print("Yes")
else:
    print("No")