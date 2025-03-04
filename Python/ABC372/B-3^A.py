M = int(input())
A = []
for i in range(10,-1,-1):
    if M//(3**i) == 1:
        A.append(i)
    elif M//(3**i) == 2:
        A.append(i)
        A.append(i)
    M =  M%(3**i)
print(len(A))
for i in range(len(A)):
    print(A[i],end=" ")
print()