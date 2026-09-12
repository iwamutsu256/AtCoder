s = list(input())
ans = []
for i in range(len(s) - 1):
    ans.append(s[i])
    ans.append("o")
ans.append(s[-1])
print("".join(ans))