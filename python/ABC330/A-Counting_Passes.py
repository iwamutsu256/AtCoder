N,L = map(int,input().split())
A = [int(x) for x in input().split()]
count = 0
for i in range(N):
    if A[i] >= L:
        count += 1
print(count)