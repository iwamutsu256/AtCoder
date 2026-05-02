S = list(input())
A = 0
B = 0
C = 0
for i in range(len(S)):
    if S[i] == "a":
        A += 1+B+C
        A = A % 998244353
    if S[i] == "b":
        B += 1+A+C
        B = B % 998244353
    if S[i] == "c":
        C += 1+A+B
        C = C % 998244353
ans = (A+B+C) % 998244353
print(ans)