T = int(input())
for i in range(T):
    N = int(input())
    A = list(map(int,input().split()))
    if N <= 2:
        print("Yes")
        continue
    a = min(A)
    b = max(A)
    if a*b > 0:
        A = sorted(A)
    else:
        A = sorted(A,key=abs)
    flag = True
    for i in range(N-2):
        if A[i]*A[i+2] != A[i+1]*A[i+1]:
            flag = False
            break
    print("Yes" if flag else "No")