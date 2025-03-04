def move(muki,num,iorj):
    if muki == "U":
        for _ in range(num):
            print("U",iorj)
            #Cの書き換え
            for i in range(N-1):
                C[i][iorj] = C[i+1][iorj]
            C[N-1][iorj] = "."
            #oni[]の座標の書き換え
            for i in range(len(oni)):
                if oni[i][1] == iorj:
                    oni[i][0] -= 1
            #oni[]の盤面外に行ったものを消去
            count = 0
            while count < len(oni):
                if oni[count][0] < 0:
                    oni.pop(count)
                else:
                    count += 1
    if muki == "D":
        for _ in range(num):
            print("D",iorj)
            #Cの書き換え
            for i in range(N-1):
                C[-1*i-1][iorj] = C[-1*i-2][iorj]
            C[0][iorj] = "."
            #oni[]の座標の書き換え
            for i in range(len(oni)):
                if oni[i][1] == iorj:
                    oni[i][0] += 1
            #oni[]の盤面外に行ったものを消去
            count = 0
            while count < len(oni):
                if oni[count][0] >= N:
                    oni.pop(count)
                else:
                    count += 1
    if muki == "R":
        for _ in range(num):
            print("R",iorj)
            #Cの書き換え
            for i in range(N-1):
                C[iorj][-1*i-1] = C[iorj][-1*i-2]
            C[iorj][0] = "."
            #oni[]の座標の書き換え
            for i in range(len(oni)):
                if oni[i][0] == iorj:
                    oni[i][1] += 1
            #oni[]の盤面外に行ったものを消去
            count = 0
            while count < len(oni):
                if oni[count][1] >= N:
                    oni.pop(count)
                else:
                    count += 1
    if muki == "L":
        for _ in range(num):
            print("L",iorj)
            #Cの書き換え
            for i in range(N-1):
                C[iorj][i] = C[iorj][i+1]
            C[iorj][N-1] = "."
            #oni[]の座標の書き換え
            for i in range(len(oni)):
                if oni[i][0] == iorj:
                    oni[i][1] -= 1
            #oni[]の盤面外に行ったものを消去
            count = 0
            while count < len(oni):
                if oni[count][1] < 0:
                    oni.pop(count)
                else:
                    count += 1

def spacecost(UorR,i,j):
    if UorR == "U":
        if C[i][j] == ".":
            cost = [0]
            return cost
        else:
            #上を調べる
            flag = True
            for k in range(1,i+1):
                if C[N-k][j] == "o":
                    flag = False
                if C[i-k][j] != "o" and flag:
                    Ucost = k
                    break
                elif C[i-k][j] != "o":
                    Ucost = 1000000
                    break
            else:
                Ucost = 1000000
            #下を調べる
            flag = True
            for k in range(1,N-i):
                if C[k-1][j] == "o":
                    flag = False
                if C[i+k][j] != "o" and flag:
                    Dcost = k
                    break
                elif C[i+k][j] != "o":
                    Dcost = 1000000
                    break
            else:
                Dcost = 1000000
            #上によけるコストと下によけるコストを比べる
            if Ucost < Dcost:
                cost = [Ucost,"D",j]
            else:
                cost = [Dcost,"U",j]
            return cost
    else:
        if C[i][j] == ".":
            cost = [0]
            return cost
        else:
            #右を調べる
            flag = True
            for k in range(1,N-j):
                if C[i][k-1] == "o":
                    flag = False
                if C[i][j+k] != "o" and flag:
                    Rcost = k
                    break
                elif C[i][j+k] != "o":
                    Rcost = 1000000
                    break
            else:
                Rcost = 1000000
            #左を調べる
            flag = True
            for k in range(1,j+1):
                if C[i][N-k] == "o":
                    flag = False
                if C[i][j-k] != "o" and flag:
                    Lcost = k
                    break
                elif C[i][j-k] != "o":
                    Lcost = 1000000
                    break
            else:
                Lcost = 1000000
            if Rcost < Lcost:
                cost = [Rcost,"L",i]
            else:
                cost = [Lcost,"R",i]
            return cost


N = int(input())
C = [list(input()) for _ in range(N)]
#print(C)
oni = []
#fuku = []
for i in range(N):
    for j in range(N):
        if C[i][j] == "x":
            oni.append([i,j])
        #if C[i][j] == "o":
        #    fuku.append([i,j])

while len(oni) > 0:
    #右脱出コスト
    rightcost = 0
    rightcost += N-oni[0][1]
    rightqueue = []
    for i in range(1,N-oni[0][1]):
        sc = spacecost("U",oni[0][0],oni[0][1]+i)
        if sc[0] != 0 and sc[0] < 10000:
            rightqueue.append(sc)
        rightcost += sc[0]
    #左脱出コスト
    leftcost = 0
    leftcost += oni[0][1]+1
    leftqueue = []
    for i in range(1,oni[0][1]+1):
        sc = spacecost("U",oni[0][0],oni[0][1]-i)
        if sc[0] != 0 and sc[0] < 10000:
            leftqueue.append(sc)
        leftcost += sc[0]
    #上脱出コスト
    upcost = 0
    upcost += oni[0][0]+1
    upqueue = []
    for i in range(1,oni[0][0]+1):
        sc = spacecost("R",oni[0][0]-i,oni[0][1])
        if sc[0] != 0 and sc[0] < 10000:
            upqueue.append(sc)
        upcost += sc[0]
    #下脱出コスト
    downcost = 0
    downcost += N-oni[0][0]
    downqueue = []
    for i in range(1,N-oni[0][0]):
        sc = spacecost("R",oni[0][0]+i,oni[0][1])
        if sc[0] != 0 and sc[0] < 10000:
            downqueue.append(sc)
        downcost += sc[0]
    #どのコストが一番安いかを比較
    cheapest = min(upcost,downcost,rightcost,leftcost)
    #print(upcost,downcost,rightcost,leftcost,cheapest)
    if cheapest >= 10000:
        re = oni.pop(0)
        oni.append(re)
    else:
        if cheapest == upcost:
            for i in range(len(upqueue)):
                move(upqueue[i][1],upqueue[i][0],upqueue[i][2])
            move("U",oni[0][0]+1,oni[0][1])
        elif cheapest == downcost:
            for i in range(len(downqueue)):
                move(downqueue[i][1],downqueue[i][0],downqueue[i][2])
            move("D",N-oni[0][0],oni[0][1])
        elif cheapest == rightcost:
            for i in range(len(rightqueue)):
                move(rightqueue[i][1],rightqueue[i][0],rightqueue[i][2])
            move("R",N-oni[0][1],oni[0][0])
        else:
            for i in range(len(leftqueue)):
                move(leftqueue[i][1],leftqueue[i][0],leftqueue[i][2])
            move("L",oni[0][1]+1,oni[0][0])
