n = int(input())
a = list(map(int,input().split()))
# 定数
MOD = 998244353
# aの累積和
b = [0 for _ in range(n+1)]
for i in range(n):
    b[i+1] = b[i] + a[i]
# 逆元の和
h = [0 for _ in range(n+1)]
for i in range(n):
    h[i+1] = h[i] + pow(i+1,MOD-2,MOD)%MOD

ans = 0
for i in range(n+1):
    ans = ( ans + b[i]*(h[i]-h[n-i]) ) % MOD
print(ans)