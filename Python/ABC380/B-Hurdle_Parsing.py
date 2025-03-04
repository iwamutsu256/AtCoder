S = input().split("|")
for i in range(len(S)-2):
    print(S[i+1].count("-"),end=" ")
print("")
