S = list(input())
sum = 1
for i in range(len(S)):
    if S[i] == "+":
        sum += 1
    elif S[i] == "-":
        sum -= 1
print(sum)