N = int(input())
W = [x for x in input().split()]
ans = False
for i in range(N):
    if W[i] == "and" or W[i] == "not" or W[i] == "that" or W[i] == "the" or W[i] == "you":
        ans = True
        break
if ans:
    print("Yes")
else:
    print("No")