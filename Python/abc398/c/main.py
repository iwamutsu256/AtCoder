N = int(input())
A = list(map(int,input().split()))
B = set()
C = set()
for i in range(N):
    if A[i] in C:
        pass
    elif A[i] in B:
        B.remove(A[i])
        C.add(A[i])
    else:
        B.add(A[i])
D = list(B)
if len(D) == 0:
    print(-1)
else:
    D.sort()
    print(A.index(D[-1])+1)