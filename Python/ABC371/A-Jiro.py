Sab,Sac,Sbc = input().split()
if Sab == ">" and Sac == ">":
    if Sbc == ">":
        print("B")
    else:
        print("C")
elif Sab == "<" and Sbc == ">":
    if Sac == ">":
        print("A")
    else:
        print("C")
else:
    if Sab == ">":
        print("A")
    else:
        print("B")
