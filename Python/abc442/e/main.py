import cmath
import math
import bisect
N,Q = map(int,input().split())
argument = []
sorted_argument = []
for i in range(N):
    X,Y = map(int,input().split())
    c = complex(X,Y)
    argument.append(cmath.phase(c))
    sorted_argument.append(cmath.phase(c))
sorted_argument.sort()
# print(sorted_argument)
for i in range(Q):
    A,B = map(int,input().split())
    A_ins = bisect.bisect_right(sorted_argument,argument[A-1])
    B_ins = bisect.bisect_left(sorted_argument,argument[B-1])
    if argument[A-1] >= argument[B-1]:
        print(A_ins - B_ins)
    else:
        print(N - B_ins + A_ins)