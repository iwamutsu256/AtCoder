from collections import defaultdict
n = int(input())
a = list(map(int,input().split()))
b = defaultdict(int)
for i in range(n):
    b[a[i]] += 1
ans = 0
# print(b)
for i in b.keys():
    if b[i] % 2 == 1:
        ans += i
print(ans)