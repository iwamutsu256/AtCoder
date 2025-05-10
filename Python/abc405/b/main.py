N,M = map(int,input().split())
A = list(map(int,input().split()))
B = set([int(x) for x in range(1,M+1)])
for i in range(0,N+1):
    if set(A) != B:
        print(i)
        break
    A.pop()
