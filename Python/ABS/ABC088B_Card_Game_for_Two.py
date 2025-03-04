N = int(input())
A = [int(x) for x in input().split()]
A.sort()
Alice = 0
Bob = 0
#print(A)
for i in range(len(A)):
    if i % 2 == 0:
        Alice += A[-1*i-1]
    else:
        Bob += A[-1*i-1]
print(Alice-Bob)