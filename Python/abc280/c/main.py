S = list(input())
T = list(input())
for i in range(min(len(S),len(T))):
    if S[i] != T[i]:
        print(i+1)
        break
else:
    print(len(T))