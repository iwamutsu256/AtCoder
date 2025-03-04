N,W = map(int,input().split())
block = [[int(x) for x in input().split()] for _ in range(N)]
mp = [[] for _ in range(W)]
for i in range(N):
    mp[block[i][0]-1].append([block[i][1],i+1])
maxlen = 0
for i in range(len(mp)):
    maxlen = max(maxlen,len(mp[i]))
for i in range(W):
    mp[i] = sorted(mp[i])
cleartime = [-1]*maxlen
for i in range(maxlen):
    for j in range(W):
        cleartime[i] = max(cleartime[i],mp[j][i][0])