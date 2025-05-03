N,M = map(int,input().split())
C = list(map(int,input().split()))
# 動物園に対して、見れる動物の種類を返す辞書を作成
dict = dict()
for i in range(M):
    K = list(map(int,input().split()))
    for j in range(1,K[0]+1):
        if K[j] in dict:
            dict[K[j]].append(i+1)
        else:
            dict[K[j]] = [i+1]
print(dict)