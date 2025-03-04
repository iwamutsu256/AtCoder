dp = [10000000000]*1000001
H = [-10000000]*100001
N = int(input())
h = list(map(int,input().split()))
for i in range(N):
    H[i+1] = h[i]
dp[1] = 0
for i in range(1,N):
    dp[i+1] = min(dp[i]+abs(H[i+1]-H[i]),dp[i-1]+abs(H[i+1]-H[i-1]))
print(dp[N])