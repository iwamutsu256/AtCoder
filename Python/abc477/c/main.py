import bisect

q = int(input())
s = input()
t = input()

# 部分文字列の先頭インデックスリスト
u = []
for i in range(len(s)-len(t)+1):
    if s[i:i+len(t)] == t:
        u.append(i)
# print(u)
for _ in range(q):
    l,r = map(int,input().split())
    l -= 1
    r -= 1
    if u == []:
        print("No")
        continue
    x = bisect.bisect_left(u,l)
    if x == len(u):
        print("No")
    elif u[x]+len(t)-1 <= r:
        print("Yes")
    else:
        print("No")