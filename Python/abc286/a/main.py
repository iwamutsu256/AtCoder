N,P,Q,R,S = map(int,input().split())
A = list(map(int,input().split()))
B = [None for _ in range(len(A))]
for i in range(N):
    if P<=i+1 and i+1<=Q:
        B[i] = str(A[R+i-P])
    elif R<=i+1 and i+1<=S:
        B[i] = str(A[P+i-R])
    else:
        B[i] = str(A[i])
print(" ".join(B))