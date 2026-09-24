n = int(input())
a = list(map(int,input().split()))

b = list(map(abs,a))

minus_cnt = 0
abs_min = min(b)
for i in range(n):
    if a[i] < 0:
        minus_cnt += 1

ans = 0

if minus_cnt % 2 == 0:
    ans = sum(b)
else:
    ans = sum(b) - abs(abs_min)*2

print(ans)