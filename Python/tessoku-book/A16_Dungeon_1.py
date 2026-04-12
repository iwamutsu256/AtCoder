N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
dp = [10*9]*100001
dp[1] = 0
for i in range(2,N+1):
    dp[i] = min(dp[i-1]+A[i-2],dp[i-2]+B[i-3])
print(dp[N])