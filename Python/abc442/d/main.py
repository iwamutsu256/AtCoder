N,Q = map(int,input().split())
A = list(map(int,input().split()))
sum_A = [0] * (N+1)
for i in range(N):
    sum_A[i+1] = sum_A[i] + A[i]
for i in range(Q):
    query = list(map(int,input().split()))
    if len(query) == 2:
        x = query[1]
        sum_A[x] += A[x]-A[x-1]
        A[x-1],A[x] = A[x],A[x-1]
    else:
        l,r = query[1],query[2]
        print(sum_A[r]-sum_A[l-1])