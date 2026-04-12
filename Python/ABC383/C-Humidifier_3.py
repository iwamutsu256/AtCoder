def func(queue):
    p = queue.pop(0)
    x = p[0]
    y = p[1]
    dis = p[2]
    S[x][y] = dis
    if y-1 >= 0 and dis < D:
        if S[x][y-1] == ".":
            queue.append((x,y-1,dis+1))
        if str(S[x][y-1]).isdigit():
            if int(S[x][y-1]) > dis+1:
                queue.append((x,y-1,dis+1))
    if y+1 <= H-1 and dis < D:
        if S[x][y+1] == ".":
            queue.append((x,y+1,dis+1))
        if str(S[x][y+1]).isdigit():
            if int(S[x][y+1]) > dis+1:
                queue.append((x,y+1,dis+1))
    if x-1 >= 0 and dis < D:
        if S[x-1][y] == ".":
            queue.append((x-1,y,dis+1))
        if str(S[x-1][y]).isdigit():
            if int(S[x-1][y]) > dis+1:
                queue.append((x-1,y,dis+1))
    if x+1 <= W-1 and dis < D:
        if S[x+1][y] == ".":
            queue.append((x+1,y,dis+1))
        if str(S[x+1][y]).isdigit():
            if int(S[x+1][y]) > dis+1:
                queue.append((x+1,y,dis+1))
    return queue

def BFS(x,y):
    q = [(x,y,0)]
    while q != []:
        q = func(q)
    #for j in range(H):
    #    print(S[j])
#入力
H,W,D = map(int,input().split())
S = [[x for x in list(input())] for _ in range(H)]

for i in range(H*W):
    if S[i//W][i%W] == "H":
        BFS(i//W,i%W)
count = 0
for j in range(H):
    #print(S[j])
    for k in range(D+1):
        count += S[j].count(k)
print(count)