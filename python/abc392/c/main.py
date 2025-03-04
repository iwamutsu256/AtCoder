N = int(input())
P = [int(x) for x in input().split()]
Q = [int(x) for x in input().split()]
R = [0]*N
for i in range(0,N):
    R[Q[i]-1] = i   
for i in range(1,N+1):
    if i != N:
        print(Q[P[R[i-1]]-1],end = " ")
    else:
        print(Q[P[R[i-1]]-1])