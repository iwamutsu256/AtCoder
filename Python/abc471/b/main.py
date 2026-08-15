from collections import defaultdict
n = int(input())
dict = defaultdict(int)
for i in range(n):
    dict[input().lower()] += 1
ans = 0
for i in dict.values():
    ans = max(ans,i)
print(ans)
