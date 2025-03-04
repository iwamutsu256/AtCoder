S = input()
count = 0
for i in range(len(S)):
    if S[i] == "v":
        count += 1
    else:
        count += 2
print(count)