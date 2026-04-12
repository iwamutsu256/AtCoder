N = int(input())
A = list(map(int,input().split()))
count = 0
now = 0
for i in range(N):
    if A[i] >= now:
        now = A[i]
    else:
        count += now - A[i]
print(count)