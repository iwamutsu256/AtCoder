N = int(input())
A = [int(x) for x in input().split()]
ans = True
if N != 2:
    for i in range(2,N):
        if A[i] * A[i-2] != A[i-1]**2:
            ans = False
if ans:
    print("Yes")
else:
    print("No")