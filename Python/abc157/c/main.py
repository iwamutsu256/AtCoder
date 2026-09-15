import sys
n,m = map(int,input().split())
num = [-1 for _ in range(n)]
for i in range(m):
    s,c = map(int,input().split())
    s -= 1
    if num[s] == -1 or num[s] == str(c):
        num[s] = str(c)
    else:
        print(-1)
        sys.exit()

if num[0] == "0":
    if n == 1:
        print(0)
        sys.exit()
    print(-1)
    sys.exit()

for i in range(n):
    if num[i] == -1:
        num[i] = "0"
# print(num)
now = str(int("".join(num)))
if len(now) < n:
    # n-len(now)桁
    now = str(10**(n-len(now)-1)) + now

print(int(now))