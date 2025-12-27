N,M = map(int,input().split())
S = list(map(int,list(input())))
T = list(map(int,list(input())))
ans = 9999
for i in range(N-M+1):
    count = 0
    for j in range(M):
        num = S[i+j] - T[j]
        if num < 0:
            num += 10
        count += num
    ans = min(ans,count)
print(ans)