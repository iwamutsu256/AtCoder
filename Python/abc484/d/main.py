from collections import defaultdict

n = int(input())
a = list(map(int,input().split()))
ans = ((n-1) * n // 2) + 1
# print(ans)
num_dict = defaultdict(int)
for i in range(n):
    if i > 0 and a[i] == a[i-1]:
        ans -= i
    else:
        ans -= num_dict[a[i]]
    num_dict[a[i]] += 1
print(ans)