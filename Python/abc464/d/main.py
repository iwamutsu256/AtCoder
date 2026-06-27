T = int(input())
for _ in range(T):
    N = int(input())
    S = list(input())
    X = [0] + list(map(int,input().split()))
    Y = [0] + list(map(int,input().split()))
    dpr = [0 for _ in range(N+1)]
    dps = [0 for _ in range(N+1)]
    for i in range(1,N+1):
        if S[i-1] == "S":
            dps[i] = max(dpr[i-1] + Y[i-1],dps[i-1])
            dpr[i] = max(dpr[i-1] - X[i],dps[i-1] - X[i])
        else:
            dps[i] = max(dps[i-1] - X[i],dpr[i-1] - X[i] + Y[i-1])
            dpr[i] = max(dpr[i-1],dps[i-1])
    # print(dps,dpr)
    print(max(dps[N],dpr[N]))