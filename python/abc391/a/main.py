D = input()
if D == "N":
    print("S")
elif D == "E":
    print("W")
elif D == "W":
    print("E")
elif D == "S":
    print("N")
elif D == "NE":
    print("SW")
elif D == "NW":
    print("SE")
elif D == "SE":
    print("NW")
else:
    print("NE")