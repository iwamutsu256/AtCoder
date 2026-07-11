n,m = map(int,input().split())
tate = [0 for _ in range(n+1)]
yoko = [0 for _ in range(n+1)]
count = 0
for i in range(m):
    r,c = map(int,input().split())
    if tate[r] != 0:
        yoko[tate[r]] = 0
        tate[r] = 0
        count -= 1
    if yoko[c] != 0:
        count -= 1
        tate[yoko[c]] = 0
        yoko[c] = 0
    tate[r] = c
    yoko[c] = r
    count += 1
print(count)
