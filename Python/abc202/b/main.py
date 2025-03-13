S = list(input())
for i in range(len(S)):
    if S[len(S)-1-i] == "6":
        print("9",end = "")
    elif S[len(S)-1-i] == "9":
        print("6",end = "")
    else:
        print(S[len(S)-1-i],end="")
print()