H,W,X,Y = map(int,input().split())
S = [list(input()) for _ in range(H)]
T = list(input())
#print(S,T)
X -= 1
Y -= 1
#print(X,Y)
count = 0
for i in range(len(T)):
    #移動可能であれば移動する
    if T[i] == "L":
        if S[X][Y-1] == ".":
            Y -= 1
        elif S[X][Y-1] == "@":
            S[X][Y-1] = "."
            count += 1
            Y -= 1
        else:
            pass
    elif T[i] == "R":
        if S[X][Y+1] == ".":
            Y += 1
        elif S[X][Y+1] == "@":
            S[X][Y+1] = "."
            count += 1
            Y += 1
        else:
            pass
    elif T[i] == "U":
        if S[X-1][Y] == ".":
            X -= 1
        elif S[X-1][Y] == "@":
            S[X-1][Y] = "."
            count += 1
            X -= 1
        else:
            pass
    elif T[i] == "D":
        if S[X+1][Y] == ".":
            X += 1
        elif S[X+1][Y] == "@":
            S[X+1][Y] = "."
            count += 1
            X += 1
        else:
            pass
    #print(S,X,Y,count)
print(X+1,Y+1,count)
