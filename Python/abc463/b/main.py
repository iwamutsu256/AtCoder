N,X = input().split()
N = int(N)
S = [list(input()) for _ in range(N)]
flag = False
if X == "A":
    X = 0
elif X == "B":
    X = 1
elif X == "C":
    X = 2
elif X == "D":
    X = 3
else:
    X = 4
for i in range(N):
    if S[i][X] == "o":
        flag = True
if flag:
    print("Yes")
else:
    print("No")