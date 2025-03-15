N = int(input())
K = list(map(int,input().split()))
ans = 10000000000
for bit in range(2**N):
    A = 0
    for i in range(N):
        if bit & 2**i:
            A += K[i]
    ans = min(ans,max(A,sum(K)-A))
print(ans)