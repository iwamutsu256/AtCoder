H,W = map(int,input().split())
S = [[x for x in input()] for _ in range(H)]
#print(S)
a = 1000
b = 1000
c = 0
d = 0
for i in range(H):
    for j in range(W):
        if S[i][j] == "#":
            a = min(a,j)
            b = min(b,i)
            c = max(c,j)
            d = max(d,i)
ans = True
for i in range(H):
    for j in range(W):
        if S[i][j] == "." and a <= j and j <= c and b <= i and i <= d:
            ans = False
#print(a,b,c,d)
if ans:
    print("Yes")
else:
    print("No")