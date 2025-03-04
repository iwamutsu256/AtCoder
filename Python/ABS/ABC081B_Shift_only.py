N = int(input())
A = list(map(int,input().split()))
count = 10000000000
for i in range(N):
    exp = 0
    while A[i] % 2 == 0:
        A[i] = A[i] // 2
        exp += 1
    count = min(count,exp)
print(count)