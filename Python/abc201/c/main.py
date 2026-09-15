s = list(input())

o_str = []
x_str = []
q_str = []
for i in range(len(s)):
    if s[i] == "o":
        o_str.append(str(i))
    elif s[i] == "x":
        x_str.append(str(i))
    else:
        q_str.append(str(i))
if len(o_str) > 4:
    print(0)
else:
    count = 0
    for i in range(10000):
        pwd = str(i).zfill(4)
        if all(o_str[j] in pwd for j in range(len(o_str))) and not any(x_str[j] in pwd for j in range(len(x_str))):
            count += 1
            print(pwd)
    print(count)
