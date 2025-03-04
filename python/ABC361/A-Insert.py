N,K,X = map(int,input().split())
A = [int(x) for x in input().split()]
for i in range(N):
    print(A[i],end=" ")
    if i == K-1:
        print(X,end =" ")
print()