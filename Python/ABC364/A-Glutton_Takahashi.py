N = int(input())
R = "salty"
A = True
for i in range(N-1):
    S = input()
    if R == "sweet" and S == "sweet":
        A = False
    R = S
S = input()
if A:
    print("Yes")
else:
    print("No")