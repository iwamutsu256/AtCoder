# matrix: 二次元配列
def rotate(matrix):
    return list(map(list,list(zip(*matrix[::-1]))))

h,w = map(int,input().split())
a = [list(input()) for _ in range(h)]

new_a = []

for i in range(h):
    flag = True
    for j in range(w):
        if a[i][j] == "#":
            flag = False
    if not flag:
        new_a.append(a[i])

new_new_a = []
new_a = rotate(new_a)
for i in range(len(new_a)):
    flag = True
    for j in range(len(new_a[0])):
        if new_a[i][j] == "#":
            flag = False
    if not flag:
        new_new_a.append(new_a[i])

ans = rotate(rotate(rotate(new_new_a)))
for i in range(len(ans)):
    print("".join(ans[i]))