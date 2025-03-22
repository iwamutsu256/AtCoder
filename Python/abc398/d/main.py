N,R,C = map(int,input().split())
S = list(input())
X = [0]
Y = [0]
for i in range(N):
    if S[i] == "N":
        X.append(X[-1]-1)
    elif S[i] == "S":
        X.append(X[-1]+1)
    else:
        X.append(X[-1])
    if S[i] == "E":
        Y.append(Y[-1]+1)
    elif S[i] == "W":
        Y.append(Y[-1]-1)
    else:
        Y.append(Y[-1])
P = set()
Q = set()
P.add(0)
Q.add(0)
X_dict = {}
Y_dict = {}
X_dict[0] = {0}
Y_dict[0] = {0}
ans = []
for i in range(N):
    if X[i+1] - R in X_dict and Y[i+1] - C in Y_dict:
        if X_dict[X[i+1] - R] & Y_dict[Y[i+1] - C]:
            ans.append("1")
        else:
            ans.append("0")
    else:
        ans.append("0")
    P.add(X[i+1])
    Q.add(Y[i+1])
    if X[i+1] not in X_dict:
        X_dict[X[i+1]] = set()
    if Y[i+1] not in Y_dict:
        Y_dict[Y[i+1]] = set()
    X_dict[X[i+1]].add(i+1)
    Y_dict[Y[i+1]].add(i+1)
print("".join(ans))