N = int(input())
For = 0
Against = 0
for i in range(N):
    S = input()
    if S == "For":
        For += 1
    else:
        Against += 1
if For > Against:
    print("Yes")
else:
    print("No")