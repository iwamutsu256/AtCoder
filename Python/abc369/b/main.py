N = int(input())
L = None
R = None
count = 0
for i in range(N):
    A,S = input().split()
    A = int(A)
    if S == "L":
        if L == None:
            L = A
        else:
            count += abs(A-L)
            L = A
    else:
        if R == None:
            R = A
        else:
            count += abs(A-R)
            R = A
print(count)