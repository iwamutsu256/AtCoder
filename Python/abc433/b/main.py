N = int(input())
A = list(map(int,input().split()))
print(-1)
for i in range(1,N):
    num = -1
    for j in range(i):
        if A[j] > A[i]:
            num = j+1
    print(num)