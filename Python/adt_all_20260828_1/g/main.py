h,w = map(int,input().split())
c = [list(input()) for _ in range(h)]
tate = [[] for _ in range(w)]
yoko = [[] for _ in range(h)]
# i個目の要素にその列の構成要素(color,count)
for i in range(h):
    for j in range(w):
        if i == 0 or tate[j][-1][0] != c[i][j]:
            tate[j].append([c[i][j],1])
        else:
            tate[j][-1][1] += 1
        if j == 0 or yoko[i][-1][0] != c[i][j]:
            yoko[i].append([c[i][j],1])
        else:
            yoko[i][-1][1] += 1
print(yoko,tate)
count = h*w
exist_tate = set(int(i) for i in range(h))
exist_yoko = set(int(i) for i in range(w))
while True:
    for i in range(h):
        if len(yoko[i]) == 1:
            