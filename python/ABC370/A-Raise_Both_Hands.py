L,R = map(int,input().split())
if L == 1 and R == 0:
    print("Yes")
elif R == 1 and L == 0:
    print("No")
else:
    print("Invalid")