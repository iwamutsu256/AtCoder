def key_func(n):
    return int(n[1])
N = int(input())
S = [tuple(input().split()) for _ in range(N)]
M = S.index(min(S, key=key_func))
for i in range(N):
    print(S[(M+i) % N][0])