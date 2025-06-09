N,L = map(int,input().split())
d = list(map(int,input().split()))
if L % 3 != 0:
    print(0)
else:
    P = {i:0 for i in range(L)}
    P[0] += 1
    current = 0
    for i in range(N-1):
        current += d[i]
        current = current % L
        P[current] += 1
    # print(P)
    ans = 0
    for i in range(L//3):
        ans += P[i] * P[i+L//3] * P[i+2*L//3]
    print(ans)