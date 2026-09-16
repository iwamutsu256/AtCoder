n = int(input())
c = list(input())
# 入れ替えが必要な回数をカウント
# 目標:R...W...
rc = 0
for i in range(n):
    if c[i] == "R":
        rc += 1
goal = ["R" for _ in range(rc)] + ["W" for _ in range(n-rc)]

ans = 0
for i in range(rc):
    if c[i] != "R":
        ans += 1
print(ans)
