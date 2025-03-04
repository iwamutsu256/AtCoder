N,M = map(int,input().split())
A = list(map(int,input().split()))
A = list(map(lambda x: x%M, A))
Saam = 0
for i in range(N):
    for j in range(N-i):
        Saam += sum(A[j:j+i+1]) % M
print(Saam)
