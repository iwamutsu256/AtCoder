n,x = map(int,input().split())
s = list(input())
now = list(bin(x)[2:])
for i in range(n):
    if s[i] == "U":
        now.pop()
    elif s[i] == "L":
        now.append("0")
    else:
        now.append("1")
now = int("".join(now),2)
print(now)