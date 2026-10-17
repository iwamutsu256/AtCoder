n,m = map(int,input().split())
s = [input() for _ in range(n)]
t = [input() for _ in range(m)]
count = [0 for _ in range(n)]
for i in range(m):
    counter = [[],[]]
    for j in range(n):
        if s[j] == t[i]:
            counter[0].append(j)
        elif len(s[j]) != len(t[i]):
            pass
        else:
            miss_counter = 0
            for k in range(len(s[j])):
                if s[j][k] != t[i][k]:
                    miss_counter += 1
            if miss_counter == 1:
                counter[1].append(j)
            else:
                pass
    if counter[0]:
        count[counter[0][0]] += 1
    elif counter[1] and len(counter[1]) == 1:
        count[counter[1][0]] += 1
for i in range(n):
    print(count[i])