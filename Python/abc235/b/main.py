N = int(input())
H = list(map(int,input().split()))
now = 0
for i in range(N):
    if H[i] <= now:
        print(now)
        break
    else:
        now = H[i]
else:
    print(now)
