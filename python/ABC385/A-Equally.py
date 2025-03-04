A = list(map(int,input().split()))
A.sort()
if A.count(A[0]) == 3 or A[0] + A[1] == A[2]:
    print("Yes")
else:
    print("No")