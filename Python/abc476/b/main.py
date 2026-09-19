n = int(input())
s = list(input())
t = list(input())

flag = True
for i in range(n):
    if t[i] == "*" or t[i] == s[i]:
        pass
    else:
        flag = False
if flag:
    print("Yes")
else:
    print("No")