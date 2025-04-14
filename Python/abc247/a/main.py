S = list(input())
for i in range(len(S)):
    if i == 0:
        print(0,end="")
    else:
        print(S[i-1],end="")
else:
    print()