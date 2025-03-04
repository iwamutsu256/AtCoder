S = input()
for i in range(8):
    if S[2*i+1] == "1":
        print("No")
        break
else:
    print("Yes")