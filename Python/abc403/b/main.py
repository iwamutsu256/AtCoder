T = list(input())
U = list(input())
V = T.copy()
W = []
for i in range(len(V)):
    if V[i] == "?":
        W.append(i)
flag = False
for i in range(26):
    if flag:
        break
    V[W[0]] = chr(ord("a")+i)
    for j in range(26):
        if flag:
            break
        V[W[1]] = chr(ord("a")+j)
        for k in range(26):
            if flag:
                break
            V[W[2]] = chr(ord("a")+k)
            for l in range(26):
                if flag:
                    break
                V[W[3]] = chr(ord("a")+l)
                if "".join(U) in "".join(V):
                    print("Yes")
                    flag = True
                    break
else:
    print("No")