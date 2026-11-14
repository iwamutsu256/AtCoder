# 商品のバーコードを3桁ずつ取ったとき、偏りがあるのかどうかを調べてみる

import sys

n,k,P,r = map(int,input().split())
# 商品のバーコード
patterns = [list(map(int,list(input()))) for _ in range(P)]
for i in range(r):
    n = input()

three_pattern = [0 for _ in range(8)]
for pattern in patterns:
    p,q,r = pattern[0],pattern[1],pattern[2]
    if (p,q,r) == (0,0,0):
        three_pattern[0] += 1
    elif (p,q,r) == (0,0,1):
        three_pattern[1] += 1
    elif (p,q,r) == (0,1,0):
        three_pattern[2] += 1
    elif (p,q,r) == (0,1,1):
        three_pattern[3] += 1
    elif (p,q,r) == (1,0,0):
        three_pattern[4] += 1
    elif (p,q,r) == (1,0,1):
        three_pattern[5] += 1
    elif (p,q,r) == (1,1,0):
        three_pattern[6] += 1
    elif (p,q,r) == (1,1,1):
        three_pattern[7] += 1
    else:
        pass
for i in range(len(three_pattern)):
    three_pattern[i] /= (P//100)

for i in range(len(three_pattern)):
    print(f"pattern {i} : {three_pattern[i]} %")

sys.exit()