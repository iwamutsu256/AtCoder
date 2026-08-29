import sys
sys.setrecursionlimit(10**8)

# 合計がnになる分け方を総当たり
def solve(keta,n):
    # 現在の係数がketaに入ってくる
    ans = []
    # print(n//keta)
    for i in range(n//keta + 1):
        if keta > 1:
            small = solve(keta-1,n-keta*i)
            for j in small:
                ans.append(j+[i])
        elif keta == 1:
            return [[n]]
    return ans

n,k = map(int,input().split())
answer = solve(n,k)
# print(answer)
answer.sort()
for i in answer:
    print(*i)