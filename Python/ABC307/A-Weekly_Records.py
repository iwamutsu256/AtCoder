N = int(input())
A = list(map(int,input().split()))
for i in range(N):
    count = 0
    for j in range(7):
        count += A[7*i+j]
    print(count,end=" ")
print()