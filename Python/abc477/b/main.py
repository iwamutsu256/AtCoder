n,d = map(int,input().split())
x = list(map(int,input().split()))

y = []
for i in range(n):
    flag = True
    for j in range(n):
        if i == j:
            continue
        if abs(x[i]-x[j]) < d:
            flag = False
    if flag:
        y.append(i+1)

print(len(y))
print(*y)