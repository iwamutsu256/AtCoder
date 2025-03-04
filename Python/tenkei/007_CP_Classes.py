import bisect
N = int(input())
A = [int(x) for x in input().split()]
Q = int(input())
A.sort()
cls = [0]
for i in range(1,N):
    cls.append((A[i-1]+A[i]+1)//2)
for i in range(Q):
    B = int(input())
    print(abs(A[bisect.bisect(cls,B)-1]-B))