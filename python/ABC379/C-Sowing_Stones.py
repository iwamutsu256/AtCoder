N,M = map(int,input().split())
X = [int(x) for x in input().split()]
A = [int(x) for x in input().split()]
if sum(A) != N:
    print(-1)
else:
    sam = 0
    for i in range(M):
        sam += A[M-i-1]*(A[M-i-1]-1)//2
        if sum(A[M-1-i:M]) > N-X[M-i-1]+1:
            print(-1)
            break
        if i>0 and X[M-i]-X[M-i-1]+1<A[M-i-1]:
            sam += (A[M-i-1]-(X[M-i]-X[M-i-1]))*A[M-i]
    else:
        print(sam)
