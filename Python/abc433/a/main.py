X,Y,Z = map(int,input().split())
while X/Y >= Z:
    if X / Y == Z:
        print("Yes")
        break
    X += 1
    Y += 1
else:
    print("No")