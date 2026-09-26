import bisect
n,q = map(int,input().split())

# 各マスについて、置いた時間、取り除いた時間
tiles = [[-1,-1] for _ in range(n)]

# クエリ2を記録する
querys = []

for i in range(1,q+1):
    k,query = input().split()
    k = int(k)
    if k == 1:
        query = int(query) - 1
        # おく
        if tiles[query] == [-1,-1] or tiles[query][1] > tiles[query][0]:
            tiles[query][0] = i
        else:
            tiles[query][1] = i
        # print(tiles)
    else:
        querys.append([i,query])

# print(tiles)
# print(querys)

querys_indexes = list(map(lambda x: x[0] , querys))
# print(querys_indexes)

colors = []
for i in range(n):
    if querys == []:
        colors.append("a")
        continue
    # 置かれていない
    if tiles[i][0] < tiles[i][1] or tiles[i][0] == -1:
        colors.append(querys[-1][1])
    # 置かれている
    else:
        x = bisect.bisect_left(querys_indexes,tiles[i][0]) - 1
        if x == -1:
            colors.append("a")
        else:
        # print(x)
            colors.append(querys[x][1])
print("".join(colors))