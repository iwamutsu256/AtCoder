S = list(input())
count = 0
for i in range(len(S)):
    if S[i] == "C":
        count += min(i+1,len(S)-i)
print(count)