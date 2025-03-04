N = int(input())
A = [int(x) for x in input().split()]
for i in range(N-1):
    print(A[i]*A[i+1],end=" ")
print()