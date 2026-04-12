N,M = map(int,input().split())
T = [False]*N
for i in range(M):
    A,B = input().split()
    A = int(A)
    if B == "F":
        print("No")
    elif T[A-1] == False:
        print("Yes")
        T[A-1] = True
    else:
        print("No")
