N = int(input())
S = input()
for i in range(len(S)):
    if len(S) % 2 == 0:
        print("No")
        break
    if i < (N-1)//2:
        if S[i] != "1":
            print("No")
            break
    elif i == (N-1)//2:
        if S[i] != "/":
            print("No")
            break
    else:
        if S[i] != "2":
            print("No")
            break
else:
    print("Yes")