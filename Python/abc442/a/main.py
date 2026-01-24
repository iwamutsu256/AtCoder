S = list(input())
count = 0
for i in range(len(S)):
    if S[i] == "i" or S[i] == "j":
        count += 1
print(count)