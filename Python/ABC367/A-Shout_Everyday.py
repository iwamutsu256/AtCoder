A,B,C = map(int,input().split())
D = [int((B+i)%24) for i in range(24)]
if D.index(B) < D.index(A) and D.index(A) < D.index(C):
    print("No")
else:
    print("Yes")