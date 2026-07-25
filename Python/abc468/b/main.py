m,d = map(int,input().split())
s = list(input())
count = 0
for i in range(m):
    flag = True
    for j in range(max(0,i-d),min(i+d+1,m)):
        if s[j] == "G":
            flag = False
    if flag:
        count += 1
print(count)