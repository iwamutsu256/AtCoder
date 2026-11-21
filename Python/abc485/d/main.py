n = int(input())
s = list(input())

if len(set(s)) != 3:
    print(0)
    exit()


flags = [False, False, False]
i = 0
while flags != [True, True, True]:
    if s[i] == "A":
        flags[0] = True
    elif s[i] == "B":
        flags[1] = True
    else:
        flags[2] = True
    i += 1
left = i
flags = [False, False, False]
i = n-1
while flags != [True, True, True]:
    if s[i] == "A":
        flags[0] = True
    elif s[i] == "B":
        flags[1] = True
    else:
        flags[2] = True
    i -= 1
right = i

if left >= right:
    print(0)
    exit()

t = s[left:right+1]
# print(left,right,t)

if len(t) <= 2 or len(set(t)) <= 2:
    print(0)
    exit()

r = 0
dict = [0,0,0]
ans = 0
for i in range(len(t)):
    while min(dict) == 0:
        if r == len(t):
            r = -1
            break
        if t[r] == "A":
            dict[0] += 1
        elif t[r] == "B":
            dict[1] += 1
        else:
            dict[2] += 1
        r += 1
    # print(len(t)-r+1)
    if r == -1:
        break
    ans += len(t) - r+1
    if t[i] == "A":
        dict[0] -= 1
    elif t[i] == "B":
        dict[1] -= 1
    else:
        dict[2] -= 1

print(ans)