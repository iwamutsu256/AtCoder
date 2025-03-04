N,P = map(int,input().split())
a = [int(x) for x in input().split()]
count = 0
for i in range(N):
    if a[i] < P:
        count += 1
print(count)