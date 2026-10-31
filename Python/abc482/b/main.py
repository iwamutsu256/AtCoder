s = [list(input()) for _ in range(5)]

ans = 5
count = 0
for i in range(5):
    if s[i][i] == "o":
        count += 1
# print(count)
ans = min(ans,5-count)
count = 0
for i in range(5):
    if s[i][4-i] == "o":
        count += 1
ans = min(ans,5-count)

for i in range(5):
    count = 0
    for j in range(5):
        if s[i][j] == "o":
            count += 1
    ans = min(ans,5-count)
for i in range(5):
    count = 0
    for j in range(5):
        if s[j][i] == "o":
            count += 1
    ans = min(ans,5-count)
print(ans)