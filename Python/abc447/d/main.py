s = list(input())
counter = [0,0,0]
for i in range(len(s)):
    if s[i] == "A":
        counter[0] += 1
    elif s[i] == "B" and counter[0] > counter[1]:
        counter[1] += 1
    elif s[i] == "C" and counter[1] > counter[2]:
        counter[2] += 1
print(counter[2])