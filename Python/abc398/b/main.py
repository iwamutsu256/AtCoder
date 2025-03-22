from collections import Counter
A = list(map(int,input().split()))
c = Counter(A)
d = list(c.values())
d.sort()
if len(d) > 1:
    if d[-1] >= 3 and d[-2] >= 2:
        print("Yes")
    else:
        print("No")
else:
    print("No")