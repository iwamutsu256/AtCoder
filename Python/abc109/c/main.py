import math

n,x = map(int,input().split())
a = list(map(int,input().split()))
a.append(x)
a = sorted(a)

ans = a[1] - a[0]

for i in range(1,len(a)):
    ans = math.gcd(ans,a[i]-a[i-1])
print(ans)