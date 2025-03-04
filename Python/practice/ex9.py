N = int(input())
# ここにプログラムを追記

a = list(map(int,input().split()))
sum = 0
for i in range(N):
    sum += a[i]
ave = sum // N
for i in range(N):
    if ave > a[i]:
        print(ave - a[i])
    else:
        print(a[i] - ave)