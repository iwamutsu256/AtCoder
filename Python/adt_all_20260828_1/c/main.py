n,m = map(int,input().split())
a = list(map(int,input().split()))
sum_x = [0 for _ in range(m)]
for _ in range(n):
    x = list(map(int,input().split()))
    for i in range(m):
        sum_x[i] += x[i]
flag = True
for i in range(m):
    if sum_x[i] < a[i]:
        flag = False
if flag:
    print("Yes")
else:
    print("No")