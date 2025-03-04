import sys

def query(prdb):
    print(len(prdb))
    for p, r, d, b in prdb:
        print(p, r, d, b)
        sys.stdout.flush()
    W, H = map(int, input().split())
    return W, H

N, T, sigma = map(int, input().split())
wh = [tuple(map(int, input().split())) for _ in range(N)]

#rng = random.Random(1234)
width = 0
height = 0
Up = 0
rotate = 0
for _ in range(T):
    prdb = []
    for i in range(N):
        #if random.randint(1,2) == 1:
        #    rotate = 1
        #else:
        #    rotate = 0
        #全体の長方形が縦長
        if width < height:
            #i番目の長方形が縦長なら
            if wh[i][0] < wh[i][1]:
                rotate = 0
            else:
                rotate = 1
            #width += wh[i][0]
            #if wh[i][1] > height:
            #    height = wh[i][1]
        #全体の長方形が横長
        else:
            if wh[i][0] < wh[i][1]:
                rotate = 1
            else:
                rotate = 0
            #height += wh[i][1]
            #if wh[i][0] > width:
            #    width = wh[i][0]
        #if i % rng == 0:
        #    Up = 1
        #    slide = -1
        #else:
        #    Up = 1
        #    slide = i - 1
        prdb.append((
            i,
            rotate,
            ['U', 'L'][Up],
            -1
            #slide,
        ))
    query(prdb)
