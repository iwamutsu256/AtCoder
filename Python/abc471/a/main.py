a,b = map(int,input().split())
if 9 in [a+b,a-b,a*b,a/b]:
    print("Nine")
else:
    print("Nein")