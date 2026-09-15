n = int(input())
a = [int(input()) for _ in range(n)]

now = 0
for i in range(n):
    next = a[now]
    if next == 2:
        print(i+1)
        break
    now = next-1
else:
    print(-1)