n = int(input())
a = list(map(int,input().split()))

colors = [0 for _ in range(9)]

for i in range(n):
    if a[i] < 400:
        colors[0] += 1
    elif a[i] < 800:
        colors[1] += 1
    elif a[i] < 1200:
        colors[2] += 1
    elif a[i] < 1600:
        colors[3] += 1
    elif a[i] < 2000:
        colors[4] += 1
    elif a[i] < 2400:
        colors[5] += 1
    elif a[i] < 2800:
        colors[6] += 1
    elif a[i] < 3200:
        colors[7] += 1
    else:
        colors[8] += 1

min_cnt = 0
max_cnt = 0

for i in range(8):
    if colors[i] > 0:
        min_cnt += 1

max_cnt = min_cnt + colors[8]

if not min_cnt and max_cnt:
    min_cnt = 1

print(min_cnt, max_cnt)