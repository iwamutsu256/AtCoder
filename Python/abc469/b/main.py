n = int(input())
s = list(input())
count = 0
for i in range(n):
    if s[i] == "x" and (i == 0 or s[i-1] == "x") and (i == n-1 or s[i+1] == "x"):
        count += 1
print(count)