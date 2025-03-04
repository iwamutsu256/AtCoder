A,B = map(int,input().split())
if A+B == A:
    print("Gold")
elif A+B == B:
    print("Silver")
else:
    print("Alloy")