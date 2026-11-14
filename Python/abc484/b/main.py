k = int(input())
a = list(map(int,input().split()))

if max(a) != 9:
    print(-1)
else:
    print(min(a))