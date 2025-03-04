N = int(input())
A = [int(x) for x in input().split()]
B = [int(x) for x in range(5000009)]
C = [0]*5000009
D = [0]*5000009
for i in range(N):
    if i != 0:
        D[i] = D[i-1]+C[i]
    if B[A[i]+B[i]+D[i]+i+1] > 0:
        C[A[i]+B[i]+D[i]+i+1] -=1
for i in range(N):
    print(max(0,A[i]+B[i]+D[i]-(N-i-1)),end=" ")
print()
