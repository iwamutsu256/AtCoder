N = int(input())
S = []
for i in range(N):
    S.append(input())
for i in range(1,51):
    for j in range(len(S)):
        if len(S[j]) == i:
            print(S[j],end = "")
print()