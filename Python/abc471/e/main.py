n,k = map(int,input().split())
a = list(map(int,input().split()))
MOD = 998244353
# 階乗のリスト
f = [1 for _ in range(n+1)]
for i in range(1,n+1):
    f[i] = (i*f[i-1])%MOD
# 階乗の逆元のリスト
g = [1 for _ in range(n+1)]
# g[n] = pow(f[n],MOD-2,MOD)
# for i in range(n,0,-1):
#     g[i-1] = (g[i] * i) % MOD

# もし、毎回powを使ったら計算量は間にあうか
for i in range(1,n+1):
    g[i] = pow(f[i],MOD-2,MOD)


# コンビネーション
def comb(x, y):
    if y < 0 or y > x:
        return 0
    return f[x] * g[y] % MOD * g[x-y] % MOD

# 2乗和
ssum = 0
for i in range(n):
    ssum += a[i]**2
    ssum %= MOD

# 異なる二つの掛け算
ssum2 = 0
sa = sum(a) % MOD
ssum2 = (sa * sa - ssum) % MOD  # Σ_{i≠j} AiAj

ans = 0
ans += comb(n-1, k-1) * ssum % MOD
if k >= 2:
    ans += comb(n-2, k-2) * ssum2 % MOD
ans %= MOD
print(ans)