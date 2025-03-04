S = input()
a,b = map(int,input().split())
T = ""
for i in range(len(S)):
    if i == a-1:
        T += S[b-1]
    elif i == b-1:
        T += S[a-1]
    else:
        T += S[i]
print(T)