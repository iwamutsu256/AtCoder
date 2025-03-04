A = list(map(int,input().split()))
B = []
for i in range(4):
    if A[i] not in B:
        B.append(A[i])
if len(B) == 3:
    print(1)
elif len(B) == 4:
    print(0)
elif len(B) == 2:
    if A.count(B[0]) == 1 or A.count(B[0]) == 3:
        print(1)
    else:
        print(2)
else:
    print(2)