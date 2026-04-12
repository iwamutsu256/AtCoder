N = int(input())
A = list(map(int,input().split()))
# ダブリング
dp = [[-1 for _ in range(N)] for _ in range(50)]
for i in range(N):
    dp[0][i] = A[i]
for d in range(1,50):
    for i in range(N):
        dp[d][i] = dp[d-1][dp[d-1][i]-1]
print(" ".join(map(str,dp[48])))