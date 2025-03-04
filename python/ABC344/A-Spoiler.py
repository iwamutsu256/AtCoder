S = input()
flag = True
for i in range(len(S)):
    if S[i] == "|":
        if flag:
            flag = False
        else:
            flag = True
    else:
        if flag:
            print(S[i],end="")
print()
