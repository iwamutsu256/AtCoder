S = list(input())
T = list(input())
if len(S) < len(T):
    while len(S) < len(T):
        S.append("")
elif len(S) > len(T):
    while len(S) > len(T):
        T.append("")
if S != T:
    for i in range(len(S)):
        if S[i] != T[i]:
            print(i+1)
            break
else:
    print(0)