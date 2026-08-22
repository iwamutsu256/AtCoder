s = input()
t = ["."]*len(s)
for i in range(len(s)):
    if s[i] == "A":
        t[i] = "A"
print(''.join(t))