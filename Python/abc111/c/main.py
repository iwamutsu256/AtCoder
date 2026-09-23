from collections import Counter

n = int(input())
v = list(map(int,input().split()))

a = []
b = []

for i in range(n):
    if i % 2 == 0:
        a.append(v[i])
    else:
        b.append(v[i])

a_c = Counter(a)
b_c = Counter(b)

a_v = []
b_v = []
for k,v in a_c.items():
    a_v.append([v,k])
for k,v in b_c.items():
    b_v.append([v,k])

a_v = sorted(a_v, reverse = True)
b_v = sorted(b_v, reverse = True)

if len(a_v) == 1:
    a_v.append([0,a_v[0][0]+1])
if len(b_v) == 1:
    b_v.append([0,b_v[0][0]+1])

ans = n+1


if a_v[0][1] != b_v[0][1]:
    ans = min(ans,(n//2 - a_v[0][0]) + (n//2 - b_v[0][0]))
else:
    ans = min(ans,(n//2 - a_v[0][0]) + (n//2 - b_v[1][0]))
    ans = min(ans,(n//2 - a_v[1][0]) + (n//2 - b_v[0][0]))

print(ans)