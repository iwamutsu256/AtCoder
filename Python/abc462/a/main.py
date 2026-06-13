S = list(input())
T = []
for i in range(len(S)):
    if S[i] in ["1","2","3","4","5","6","7","8","9","0"]:
        T.append(S[i])
print("".join(T))