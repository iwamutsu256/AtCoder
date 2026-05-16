H,W = map(int,input().split())
S = [[0 for _ in range(W)] for _ in range(H)]
for i in range(H):
    for j in range(W):
        count = 0
        for (x,y) in [(1,0),(0,1),(-1,0),(0,-1)]:
            if 0<=i+x<=H-1 and 0 <= j+y <= W-1:
                count += 1
        S[i][j] = count
for i in range(H):
    print(" ".join(map(str,S[i])))