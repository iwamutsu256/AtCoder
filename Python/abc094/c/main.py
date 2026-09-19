n = int(input())
x = list(map(int,input().split()))

y = sorted(x)
mid = (y[n//2 - 1] + y[n//2])/2

for i in range(n):
    if x[i] < mid:
        print(y[n//2])
    else:
        print(y[n//2 - 1])
