a = list(map(int,input().split()))
b = [int(x) for x in range(1,6)]
diff_count = 0
diffs = []
for i in range(5):
    if a[i] != b[i]:
        diff_count += 1
        diffs.append(i)
if diff_count == 2:
    if diffs[1] - diffs[0] == 1:
        print("Yes")
    else:
        print("No")
else:
    print("No")