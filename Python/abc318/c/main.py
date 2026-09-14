n,d,p = map(int,input().split())
f = list(map(int,input().split()))
f = sorted(f, reverse=True)
cost = sum(f)

now = 0
pass_count = 0
while now <= n:
    if sum(f[now:min(now+d,n)]) > p:
        now = min(now+d,n)
        pass_count += 1
    else:
        break
if now == n:
    print(pass_count * p)
else:
    print(pass_count*p + sum(f[now:]))