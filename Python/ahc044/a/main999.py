import sys
input = sys.stdin.readline

def calctsa(TG):
    score=0

    for i in range(N):
        score+=abs(TG[i]-T[i])

    return score

N,L=map(int,input().split())
T=list(map(int,input().split()))

TX=[(T[i],i) for i in range(N)]
TX.sort(reverse=True)

def calc(SA,NOW,first):
    for i in range(first,N):
        t,ind=TX[i]
        LIST=[]
        u=T[ind]//2

        LIST2=[]
        for j in range(N):
            if j==ind:
                continue
            LIST.append((T[j]-NOW[j],j))
            if T[j]-NOW[j]>0 and abs(T[j]-NOW[j]-u)<SA[i]:
                LIST2.append((abs(T[j]-NOW[j]-u),j))

        LIST.sort()
        LIST2.sort(reverse=True)

        if LIST2 and LIST2[-1][0]<SA[i]:
            w,xind=LIST2.pop()
            NOW[xind]+=T[ind]//2
        else:
            w,xind=LIST.pop()
            NOW[xind]+=T[ind]//2

        if LIST2 and LIST2[-1][0]<SA[i]:
            w,xind=LIST2.pop()
            NOW[xind]+=T[ind]-T[ind]//2
        else:
            w,xind=LIST.pop()
            NOW[xind]+=T[ind]-T[ind]//2

    return calctsa(NOW)

ANS=[[-1,-1] for i in range(N)]
NOW=[0]*N


SA=[30]*N
for i in range(N):
    t,ind=TX[i]

    BEST=1<<30
    bestj=-1
    bestk=-1

    LIST=[]
    u=T[ind]//2

    LIST2=[]
    for j in range(N):
        if j==ind:
            continue
        LIST.append((T[j]-NOW[j],j))
        if T[j]-NOW[j]>0 and abs(T[j]-NOW[j]-u)<SA[i]:
            LIST2.append((abs(T[j]-NOW[j]-u),j))

    LIST.sort(reverse=True)
    LIST2.sort()

    LL=[]
    for ix in range(2):
        LL.append(LIST[ix][1])

        if ix<len(LIST2):
            LL.append(LIST2[ix][1])

    for j in LL:
        if ind==j:
            continue
        for k in LL:
            if ind==k:
                continue
            if j==k:
                continue
            NOW2=NOW[:]
            NOW2[j]+=T[ind]//2
            NOW2[k]+=T[ind]-T[ind]//2

            score=calc(SA,NOW2,i+1)

            if score<BEST:
                BEST=score
                bestj=j
                bestk=k

    ANS[ind][0]=bestj
    ANS[ind][1]=bestk
    NOW[bestj]+=T[ind]//2
    NOW[bestk]+=T[ind]-T[ind]//2


LANS=[]
for x,y in ANS:
    LANS.append(str(x)+" "+str(y))

print("\n".join(LANS))
