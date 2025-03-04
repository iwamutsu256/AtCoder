N = int(input())
nowT,nowX,nowY = 0,0,0
flag = True
for i in range(N):
    nextT,nextX,nextY = map(int,input().split())
    disX = abs(nowX-nextX)
    disY = abs(nowY-nextY)
    disT = nextT-nowT
    dis = disX+disY
    if dis > disT or (dis-disT)%2 == 1:
        flag = False
    nowX = nextX
    nowY = nextY
    nowT = nextT
if flag:
    print("Yes")
else:
    print("No")
