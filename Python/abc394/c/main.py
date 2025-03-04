S = input()
W_count = 0
flag_W = False
for i in range(len(S)):
    if S[i] == "W":
        if flag_W:
            W_count += 1
        else:
            flag_W = True
            W_count = 1
    elif S[i] == "A":
        if flag_W:
            print("A",end = "")
            for _ in range(W_count):
                print("C",end = "")
            flag_W = False
            W_count = 0
        else:
            print(S[i],end = "")
    else:
        for _ in range(W_count):
            print("W",end = "")
        flag_W = False
        W_count = 0
        print(S[i],end = "")
for i in range(W_count):
    print("W",end = "")
print()