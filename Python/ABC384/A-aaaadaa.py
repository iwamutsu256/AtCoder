N,c1,c2 = input().split()
S = list(input())
N = int(N)
for i in range(N):
    if S[i] != c1:
        S[i] = c2
print("".join(S))
