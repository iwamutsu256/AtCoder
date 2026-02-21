T = int(input())
for _ in range(T):
    N,D = map(int,input().split())
    A = list(map(int,input().split()))
    B = list(map(int,input().split()))
    syouhi_sum = [0]
    for i in range(len(B)):
        syouhi_sum.append(syouhi_sum[i] + B[i])
    # print(syouhi_sum)
    dp = [0] * (N+1)
    # 消費用dp2
    dp2 = [0] * (N+1)
    for i in range(1,N+1):
        if i <= D:
            dp[i] = dp[i-1] + A[i-1] - B[i-1]
            dp2[i] = dp2[i-1]
        else:
            Z = syouhi_sum[i] - syouhi_sum[i-D] + dp2[i-1] - dp2[i-D]
            if dp[i-D] >= Z:
                dp[i] = dp[i-1] + A[i-1] - B[i-1] - (dp[i-D] - Z)
                dp2[i] = dp2[i-1] + dp[i-D] - Z
            else:
                dp[i] = dp[i-1] + A[i-1] - B[i-1]
                dp2[i] = dp2[i-1]
    print(dp[N])