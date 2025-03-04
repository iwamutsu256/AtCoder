A = [int(x) for x in input().split()]
flag = False
if A[0] * A[1] == A[2]:
    flag = True
if A[0] * A[2] == A[1]:
    flag = True
if A[1] * A[2] == A[0]:
    flag = True
if flag:
    print("Yes")
else:
    print("No")