from collections import deque

n = int(input())
a = list(map(int,input().split()))

b = deque([])
inverse = 0

for i in range(n):
    if inverse:
        b.appendleft(a[i])
    else:
        b.append(a[i])
    inverse ^= 1
if inverse:
    b = reversed(b)

print(*b)