N,Q = map(int,input().split())
su = [1]*N
hato = [int(x+1) for x in range(N)]
sam = 0
for i in range(Q):
    query = input().split()
    for j in range(len(query)):
        query[j] = int(query[j])
    #print(query)
    if query[0] == 1:
        #ふえるとき
        if (su[hato[query[1]-1]-1] == 1 and su[query[2]-1] == 1) or (su[hato[query[1]-1]-1] > 2 and su[query[2]-1] == 1):
            sam += 1
        elif (su[hato[query[1]-1]-1] == 2 and su[query[2]-1] == 0) or (su[hato[query[1]-1]-1] == 2 and su[query[2]-1] >= 2):
            sam -= 1
        su[hato[query[1]-1]-1] -= 1
        su[query[2]-1] += 1
        hato[query[1]-1] = query[2]
    else:
        print(sam)