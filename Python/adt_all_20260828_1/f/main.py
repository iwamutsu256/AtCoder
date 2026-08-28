def cross(x1,y1,x2,y2):
    return x1*y2 - x2*y1

def is_convex(n, vertexes):
    #n多角形の判定
    flg = True #入力された図形が凸ならTrue/凸でないならFalse
    for i in range(n):
        #3頂点を時計回りに参照
        a = vertexes[i%n]
        b = vertexes[(i+1)%n]
        c = vertexes[(i+2)%n]

        #ベクトルab, bcを計算
        vec_ab = [b[0]-a[0], b[1]-a[1]]
        vec_bc = [c[0]-b[0], c[1]-b[1]]

        #外積が
        if cross(*vec_ab, *vec_bc)<0:
            flg = False
            break
    #flg=True の場合は凸多角形、Falseは凸でない多角形
    return flg

vertexes = []
for i in range(4):
    vertexes.append(list(map(int,input().split())))

flag = is_convex(4, vertexes)
if flag:
    print("Yes")
else:
    print("No")