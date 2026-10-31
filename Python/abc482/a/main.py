s = list(input())
count = 0
for i in s:
    if i == "o":
        count += 1
if count  %2 == 0:
    print("even")
else:
    print("odd")