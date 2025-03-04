N = int(input())
A = [int(x) for x in input().split()]
count = 0
for i in range(N):
    if A[i] % 2 == 1:
        count += 1
if count % 2 == 1:
    print("NO")
else:
    print("YES")
