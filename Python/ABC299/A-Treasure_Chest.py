N = int(input())
S = input()
flag = False
for i in range(N):
    if flag and S[i] == "*":
        print("in")
        break
    if S[i] == "|":
        if flag:
            flag = False
        else:
            flag = True
else:
    print("out")