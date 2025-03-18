A,B = map(int,input().split())
S = str(B/A)
if len(S) > 5:
    if int(S[5]) >= 5:
        S = str(float(S[:5])+0.001)
    else:
        S = str(float(S[:5]))
elif len(S) < 5:
    for i in range(5-len(S)):
        S += "0"
else:
    pass
print(S)
    