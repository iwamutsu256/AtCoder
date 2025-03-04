N,P,Q = map(int,input().split())
D = [int(x) for x in input().split()]
D.sort()
if D[0] + Q < P:
    print(D[0] + Q)
else:
    print(P)