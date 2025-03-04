from collections import deque
S = input()
T = deque([])
for i in range(len(S)):
    if S[i] == "(":
        T.append("(")
    elif S[i] == "[":
        T.append("[")
    elif S[i] == "<":
        T.append("<")
    else:
        if len(T) > 0:
            U = T.pop()
            if S[i] == ")":
                if U != "(":
                    print("No")
                    break
            elif S[i] == "]":
                if U != "[":
                    print("No")
                    break
            elif S[i] == ">":
                if U != "<":
                    print("No")
                    break
        else:
            print("No")
            break
else:
    if len(T) == 0:
        print("Yes")
    else:
        print("No")