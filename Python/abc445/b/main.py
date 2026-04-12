N = int(input())
S = [input() for _ in range(N)]
m = 0
for i in range(N):
    if len(S[i]) > m:
        m = len(S[i])
for i in range(N):
    k = (m - len(S[i]))//2
    T = "."*k + S[i] + "."*k
    print(T)