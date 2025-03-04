def g(n):
    #i桁目までで、先頭がj,n以下確定か
    dp = [[[0,0] for _ in range(int(n[0])+1)] for _ in range(len(n)+1)]
    for i in range(len(n)):
        for j in range(1,int(n[0])+1):
            if i == 0 and j == int(n[0]):
                dp[i+1][j][0] += 1
            elif i == 0:
                dp[i+1][j][1] += 1
            for k in range(0,j):
                if j < int(n[0]) or k < int(n[i]):
                    dp[i+1][j][1] += dp[i][j][0] + dp[i][j][1]
                elif k == int(n[i]):
                    dp[i+1][j][1] += dp[i][j][1]
                    dp[i+1][j][0] += dp[i][j][0]
                else:
                    dp[i+1][j][1] += dp[i][j][1]
    res = 0
    for i in range(1,int(n[0])+1):
        res += sum(dp[-1][i])
    return res

def f(n):
    if n < 10:
        return 0
    res = 0
    n = str(n)
    for i in range(2,len(n)):
        for j in range(1,10):
            res += j ** (i-1)
    res += g(n)
    return res

l,r = map(int,input().split())
print(f(r)-f(l-1))