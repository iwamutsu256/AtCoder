def printd(muki,num,iorj):
    if muki == "U":
        for _ in range(num):
            print("U",iorj)
        for _ in range(num):
            print("D",iorj)
    if muki == "D":
        for _ in range(num):
            print("D",iorj)
        for _ in range(num):
            print("U",iorj)
    if muki == "R":
        for _ in range(num):
            print("R",iorj)
        for _ in range(num):
            print("L",iorj)
    if muki == "L":
        for _ in range(num):
            print("L",iorj)
        for _ in range(num):
            print("R",iorj)

N = int(input())
C = [list(input()) for _ in range(N)]
#print(C)
oni = []
fuku = []
for i in range(N):
    for j in range(N):
        if C[i][j] == "x":
            oni.append([i,j])
        if C[i][j] == "o":
            fuku.append([i,j])
#print(oni,fuku)
#それぞれの鬼に対して、どの向きが空いているかを調べる
for i in range(2*N):
    muki = ""
    #右
    flag = True
    for j in range(1,N-oni[i][1]):
        if C[oni[i][0]][oni[i][1]+j] == "o":
            flag = False
    if flag:
        muki = "R"
        printd(muki,N-oni[i][1],oni[i][0])
    #左
    flag = True
    for j in range(oni[i][1]):
        if C[oni[i][0]][j] == "o":
            flag = False
    if flag:
        muki = "L"
        printd(muki,oni[i][1]+1,oni[i][0])
    #上
    flag = True
    for j in range(oni[i][0]):
        if C[j][oni[i][1]] == "o":
            flag = False
    if flag:
        muki = "U"
        printd(muki,oni[i][0]+1,oni[i][1])
    #下
    flag = True
    for j in range(1,N-oni[i][0]):
        if C[oni[i][0]+j][oni[i][1]] == "o":
            flag = False
    if flag:
        muki = "D"
        printd(muki,N-oni[i][0],oni[i][1])
    