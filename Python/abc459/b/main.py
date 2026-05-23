N = int(input())
S = list(input().split())
C = []
for i in range(len(S)):
    top = S[i][0]
    if top in ["a","b","c"]:
        C.append("2")
    elif top in ["d","e","f"]:
        C.append("3")
    elif top in ["g","h","i"]:
        C.append("4")
    elif top in ["j","k","l"]:
        C.append("5")
    elif top in ["m","n","o"]:
        C.append("6")
    elif top in ["p","q","r","s"]:
        C.append("7")
    elif top in ["t","u","v"]:
        C.append("8")
    elif top in ["w","x","y","z"]:
        C.append("9")
print("".join(C))