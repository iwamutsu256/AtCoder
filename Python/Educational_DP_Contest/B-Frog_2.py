dp = [10000000000]*1000001
H = [-10000000]*100001
N,K = map(int,input().split())
h = list(map(int,input().split()))
for i in range(N):
    H[i+1] = h[i]
dp[1] = 0
for i in range(1,N):
    for j in range(1,K+1):
        dp[i+1] = min(dp[i+1-j]+abs(H[i+1]-H[i+1-j]),dp[i+1])
print(dp[N])