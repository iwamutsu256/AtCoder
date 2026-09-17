import sys
n = int(input())

a = [int(input()) for _ in range(n)]

a = sorted(a)

ans = sum(a)

if ans % 10 != 0:
    print(ans)
    sys.exit()

for i in range(n):
    if a[i] % 10 != 0:
        print(ans-a[i])
        sys.exit()
else:
    print(0)
