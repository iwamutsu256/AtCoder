n = int(input())
a = list(map(int,input().split()))
b = list(map(int,input().split()))
c = [a[i]-b[i] for i in range(n)]
for i in range(n):
    if c[i] > 0:
        ans = [1 for _ in range(i)] + [10**18] + [1 for _ in range(n-i-1)]
        print("Yes")
        print(*ans)
        exit()
else:
    print("No")