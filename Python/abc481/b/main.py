n,k = map(int,input().split())
a = list(map(int,input().split()))
ans = 0
if a[0] == k:
    ans += 1
for i in range(n-1):
    if (a[i] < k and a[i+1] > k) or (a[i] > k and a[i+1] < k) or a[i+1] == k:
        ans += 1
print(ans)