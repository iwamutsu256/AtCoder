h,w = map(int,input().split())
s = [list(input()) for _ in range(h)]
komas = []
for i in range(h):
    for j in range(w):
        if s[i][j] == "o":
            komas.append((j,i))
ans = abs(komas[0][0]-komas[1][0]) + abs(komas[0][1]-komas[1][1])
# print(komas)
print(ans)