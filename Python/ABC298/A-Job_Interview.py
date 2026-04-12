N = int(input())
S = input()
ryou = False
fuka = True
for i in range(N):
    if S[i] == "o":
        ryou = True
    if S[i] == "x":
        fuka = False
if ryou and fuka:
    print("Yes")
else:
    print("No")
    