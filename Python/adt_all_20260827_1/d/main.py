n = int(input())
a = [list(map(int,input().split())) for _ in range(n)]

now = 1
for i in range(1,n+1):
    j,k = max(now,i),min(now,i)
    now = a[j-1][k-1]
print(now)