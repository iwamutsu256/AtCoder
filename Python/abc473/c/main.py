from collections import defaultdict
n,k = map(int,input().split())
a = list(map(int,input().split()))
b = defaultdict(int)
big = 0
for i in range(n):
    b[a[i]] += 1
    big = max(big,b[a[i]])
count = 0
for v in b.values():
    if v == big or v == big-1:
        count += 1
print(count)