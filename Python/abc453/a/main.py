N = int(input())
S = list(input())
i = 0
while i <= N-1 and S[i] == "o":
    i += 1
print("".join(S[i:]))