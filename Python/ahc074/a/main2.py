# ２つの窓の値だけを持つ紙を128枚作る
# 各クエリに対して、最大32回の操作で可能
# 最大スコア T = 32*1024 = 65536//2

import sys

n,k,p,r = map(int,input().split())
# 商品のバーコード
patterns = [list(input()) for _ in range(p)]

paper = []
for i in range(2*n):
    keta = i//2
    pattern = ["."]*n
    if i % 2 == 0:
        pattern[keta] = "0"
    else:
        pattern[keta] = "1"
    paper.append("".join(pattern))
for i in range(k-2*n):
    pattern = ["."]*n
    paper.append("".join(pattern))

for pattern in paper:
    print(pattern)
sys.stdout.flush()

current_pattern = ["0" for _ in range(n)]

for _ in range(r):
    request = int(input())
    if request == -1:
        sys.exit()
    target_pattern = patterns[request]
    moves = []
    for i in range(n):
        if current_pattern[i] != target_pattern[i]:
            if current_pattern[i] == "0":
                paper_num = 2*i
                current_pattern[i] = "1"
            else:
                paper_num = 2*i+1
                current_pattern[i] = "0"
            moves.append((paper_num,127))
    print(len(moves))
    for move in moves:
        print(*move)
    sys.stdout.flush()