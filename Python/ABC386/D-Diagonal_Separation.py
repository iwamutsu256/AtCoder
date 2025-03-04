N,M = map(int,input().split())
Map = []
for i in range(M):
    X,Y,C = input().split()
    #X行Y列
    X = int(X)
    Y = int(Y)
    Map.append((X,Y,C))
#行についてみる
gyou = True
retsu = True
max = N
now = 0
Map.sort(key=lambda x:(x[0],-x[1]))
for i in range(M):
    if gyou == True:
        now = Map[i][0]
        if Map[i][2] == "W" and Map[i][1] <= max:
            gyou = False
        if Map[i][2] == "B" and Map[i][1] <= max:
            max = Map[i][1]
        if Map[i][2] == "B" and Map[i][1] < max:
            gyou = False
        #elif Map[i][2] == "W" and Map[i][1]-1 <= max:
            #max = Map[i][1]-1
        #else:
        #    gyou = False
now = 0
max = N
Map.sort(key=lambda y:(y[1],-y[0]))
for i in range(M):
    if retsu == True:
        now = Map[i][1]
        if Map[i][2] == "W" and Map[i][0] <= max:
            retsu = False
        if Map[i][2] == "B" and Map[i][0] <= max:
            max = Map[i][0]
        if Map[i][2] == "B" and Map[i][0] > max:
            retsu = False
        #elif Map[i][2] == "W" and Map[i][0]-1 <= max:
            #max = Map[i][0]-1
        #else:
        #    retsu = False
if gyou and retsu:
    print("Yes")
else:
    print("No")
