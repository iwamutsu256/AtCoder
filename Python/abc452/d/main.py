def check(S,T):
    i = 0
    for t in T:
        while i < len(S) and S[i] != t:
            i += 1
        if i == len(S):
            return False
        i += 1
    return True
S = input()
T = input()
R = [0 for _ in range(len(S))]
for i in range(len(S)):
    if i == 0:
        R[i] = 0
    else:
        R[i] = R[i-1]
    while R[i] < len(S) and not check(S[i:R[i]+1],T):
        R[i] += 1
ans = 0
for i in range(len(S)):
    ans += R[i] - i
print(ans)