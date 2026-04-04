N = int(input())
A = []
B = []
for i in range(N):
    a,b = map(int,input().split())
    A.append(a)
    B.append(b-1)
M = int(input())
S_list = []
for i in range(M):
    s = list(input())
    S_list.append(s)

# 長さNのset()の配列に文字を保存
char_list = [set() for _ in range(N)]
# max2000000
for i in range(N):
    for j in range(M):
        if len(S_list[j]) == A[i]:
            char_list[i].add(S_list[j][B[i]])

for i in range(M):
    target = S_list[i]
    flag = True
    if len(target) != N:
        print("No")
        continue
    for j in range(N):
        if S_list[i][j] not in char_list[j]:
            flag = False
    if flag:
        print("Yes")
    else:
        print("No")