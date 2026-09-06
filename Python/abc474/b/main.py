n = int(input())
p = list(map(int,input().split()))
flag = True
for i in range(n):
    team = (i) // 10
    # print(team)
    if (p[i]-1) // 10 != team:
        flag = False
if flag:
    print("Yes")
else:
    print("No")