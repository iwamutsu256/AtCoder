def distance(W,H,x,y):
    dis_x = abs(W-x)
    dis_y = abs(H-y)
    dis = dis_x + dis_y
    return dis

def kasitsu_count(W,H,D,x,y,x2,y2):
    count = 0
    for i in range(H):
        for j in range(W):
            if S[i][j] == "." and (distance(j,i,x,y) <= D or distance(j,i,x2,y2) <= D):
                count += 1
    return count


H,W,D = map(int,input().split())
S = [[x for x in list(input())] for i in range(H)]
max = 0
for i in range(H*W):
    for j in range(i+1,H*W):
        if S[i // W][i % W] =="." and S[j // W][j % W] == ".":
            counter = kasitsu_count(W,H,D,i%W,i//W,j%W,j//W)
            if max < counter:
                max = counter
print(max)