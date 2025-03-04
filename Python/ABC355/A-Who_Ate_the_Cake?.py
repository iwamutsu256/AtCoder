A,B = map(int,input().split())
if A != B:
    if A + B == 3:
        print(3)
    elif A + B == 4:
        print(2)
    else:
        print(1)
else:
    print(-1)