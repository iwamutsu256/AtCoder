S = list(input())
count = -1
for i in range(len(S)):
    if S[i] == "a":
        count = i+1
print(count)