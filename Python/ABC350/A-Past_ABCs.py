S = input()
if S == "ABC316" or S == "ABC000":
    print("No")
else:
    if int(S[3]) < 3:
        print("Yes")
    elif int(S[3]) > 3:
        print("No")
    else:
        if int(S[4]) < 5:
            print("Yes")
        else:
            print("No")
