n,m = map(int,input().split())
a = [0] + list(map(int,input().split()))
sum_a = [0 for _ in range(n+1)]
for i in range(1,n+1):
    sum_a[i] = sum_a[i-1] + a[i]
score = 0
for i in range(1,m+1):
    score += i*a[n-m+i]
ans = score
for i in range(n-m-1,-1,-1):
    score -= m*a[i+m+1]
    score += sum_a[i+m]-sum_a[i]
    ans = max(score,ans)
print(ans)