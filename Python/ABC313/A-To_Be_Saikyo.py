N = int(input())
P = [int(x) for x in input().split()]
one = P[0]
del P[0]
if len(P)>0:
    P.sort()
    if P[-1] - one < 0:
        print(0)
    else:
        print(P[-1]-one+1)
else:
    print(0)