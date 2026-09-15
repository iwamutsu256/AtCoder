s = list(input())
k = int(input())
one_count = 0
while one_count < len(s) and s[one_count] == "1":
    one_count += 1
if k <= one_count:
    print(1)
else:
    print(s[one_count])