n, m = map(int,input().split())
s = [list(input()) for _ in range(n)]

# matrix: 二次元配列
def rotate(matrix):
    return list(map(list,list(zip(*matrix[::-1]))))

t = rotate(s)

for i in range(n):
    if s[i] == ["x" for _ in range(m)]:
        print("Faucet",i+1)
        exit()

for i in range(m):
    if t[i] == ["x" for _ in range(n)]:
        print("Drain", i+1)
        exit()