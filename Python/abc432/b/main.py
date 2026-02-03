X = list(map(int,list(input())))
X.sort()
nZ = 0
while True:
    if X[nZ] != 0:
        break
    nZ += 1
X[nZ],X[0] = X[0],X[nZ]
print("".join(map(str,X)))