A = list(input().split())
B = list(dict.fromkeys(A))
if len(B) == 2:
    print("Yes")
else:
    print("No")