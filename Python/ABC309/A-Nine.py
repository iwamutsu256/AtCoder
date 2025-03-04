A,B = map(int,input().split())
if A % 3 == 1:
    if B - A == 1:
        print("Yes")
    else:
        print("No")
elif A % 3 == 0:
    if B - A == -1:
        print("Yes")
    else:
        print("No")
else:
    if abs(B - A) == 1:
        print("Yes")
    else:
        print("No")
