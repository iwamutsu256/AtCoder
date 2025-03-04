def gousei(a,b):
    if a > b:
        return A[a-1][b-1]
    else:
        return A[b-1][a-1]

N = int(input())
A = [[int(x) for x in input().split()] for i in range(N)]
now = 1
for i in range(N):
    now = gousei(now,i+1)
print(now)