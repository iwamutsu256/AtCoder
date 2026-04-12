N,P,Q = map(int,input().split())
A = [int(x) for x in input().split()]
count = 0
for i in range(N-4):
    for j in range(i+1,N-3):
        for k in range(j+1,N-2):
            for l in range(k+1,N-1):
                for m in range(l+1,N):
                    if ((A[i]%P)*(A[j]%P)*(A[k]%P)*(A[l]%P)*(A[m]%P))%P == Q:
                        count += 1
print(count)