s = list(input())

dp = [0 for _ in range(8)]

for i in range(len(s)):
    if s[i] == "c":
        dp[0] += 1
    elif s[i] == "h":
        dp[1] += dp[0]
    elif s[i] == "o":
        dp[2] += dp[1]
    elif s[i] == "k":
        dp[3] += dp[2]
    elif s[i] == "u":
        dp[4] += dp[3]
    elif s[i] == "d":
        dp[5] += dp[4]
    elif s[i] == "a":
        dp[6] += dp[5]
    elif s[i] == "i":
        dp[7] += dp[6]
print(dp[7]%(10**9+7))