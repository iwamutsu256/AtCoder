N = int(input())
S = input()
ans = True
for i in range(1,N):
    if S[i] == "M" and S[i-1] == "M":
        ans = False
        break
    if S[i] == "F" and S[i-1] == "F":
        ans = False
        break
if ans:
    print("Yes")
else:
    print("No")
