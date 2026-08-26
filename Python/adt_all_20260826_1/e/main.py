n = int(input())
a = list(map(int,input().split()))
dp = [[0 for _ in range(n)] for _ in range(100)]
for i in range(n):
    dp[0][i] = a[i]-1

for j in range(1,100):
    for i in range(n):
        dp[j][i] = dp[j-1][dp[j-1][i]]
# print(dp)
print(*list(map(lambda x: x+1, dp[99])))