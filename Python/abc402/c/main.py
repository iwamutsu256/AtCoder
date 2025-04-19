N,M = map(int,input().split())
K = [list(map(int,input().split())) for _ in range(M)]
B = list(map(int,input().split()))
ans = [0]* N
# 食材iを克服する日の辞書
dict = {}
for i in range(N):
    dict[B[i]] = i+1
for i in range(M):
    maximum = 0
    for j in range(K[i][0]):
        # 最遅克服日を線形探索によって求める
        maximum = max(maximum,dict[K[i][j+1]])
    ans[maximum-1] += 1
current = 0
for i in range(N):
    current += ans[i]
    print(current)