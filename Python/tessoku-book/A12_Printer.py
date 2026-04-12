def time(t):
    ans = 0
    for i in range(N):
        ans += t//A[i]
    return ans

N,K = map(int,input().split())
A = [int(x) for x in input().split()]
L = 0
R = 1000000000
answer = -1
while answer < 0:
    if R-L == 0:
        answer = R
    center = (R+L)//2
    if time(center) >= K:
        R = center
    elif time(center) < K:
        L = center + 1
print(answer)