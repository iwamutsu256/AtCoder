A = list(map(int,input().split()))
B = sorted(A)
if A[1] == B[1]:
    print("Yes")
else:
    print("No")