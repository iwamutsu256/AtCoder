import bisect

n, s, l = map(int,input().split())
a = [0] + list(map(int,input().split()))

sum_a = [0 for _ in range(n)]
for i in range(n-1):
    sum_a[i+1] = sum_a[i] + a[i+1]

sum_b = [sum_a[i] - sum_a[s-1] for i in range(n)]

# print(sum_a,sum_b)

ans = 0

# case 1
# 全部左
town_num = bisect.bisect_left(sum_b, -l) + 1
ans = max(ans, s-town_num+1)
# print(s-town_num+1)

# case 2
# 全部右
# print(sum_b,l)
town_num = bisect.bisect_right(sum_b, l)
ans = max(ans, town_num-s+1)
# print(town_num)
# print(town_num-s+1)
# case 3
# 左右
for i in range(s-1):
    for j in range(n-s):
        if sum_a[s-1] - sum_a[i] + sum_a[s+j] - sum_a[i] <= l:
            ans = max(ans, s+j-i+1)
            # print(s+j-i+1)


for i in range(s-1):
    for j in range(n-s):
        if sum_a[s+j] - sum_a[i] + sum_a[s+j] - sum_a[s-1] <= l:
            ans = max(ans, s+j-i+1)
            # print(s+j-i+1)

print(ans)
