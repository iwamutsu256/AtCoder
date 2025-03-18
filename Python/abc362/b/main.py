A = list(map(int,input().split()))
B = list(map(int,input().split()))
C = list(map(int,input().split()))
L = [((A[0]-B[0])**2+(A[1]-B[1])**2),((B[0]-C[0])**2+(B[1]-C[1])**2),((C[0]-A[0])**2+(C[1]-A[1])**2)]
L.sort()
if L[0]+L[1] == L[2]:
    print("Yes")
else:
    print("No")