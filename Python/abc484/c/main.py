import sys
from collections import Counter


n = int(input())
a = list(map(int,input().split()))
b = list(map(int,input().split()))

ca = Counter(a)
cb = Counter(b)

if a == b:
    print("Yes")
    sys.exit()

if ca != cb:
    print("No")
    sys.exit()

back_flag = False
# 後ろにずれる
status = 0
for i in range(n):
    if a[i] != b[i] and status == 0:
        status = 1
        move_char = a[i]
    elif a[i] != b[i-1] and status == 1:
        if b[i-1] != move_char:
            break
        if b[i] != a[i]:
            break
        status = 2
    elif status == 2 and a[i] != b[i]:
        break
else:
    back_flag = True


front_flag = False
# 前にずれる
status = 0
for i in range(n):
    if a[i] != b[i] and status == 0:
        status = 1
        move_char = b[i]
    elif a[i-1] != b[i] and status == 1:
        if a[i-1] != move_char:
            break
        if b[i] != a[i]:
            break
        status = 2
    elif status == 2 and a[i] != b[i]:
        break
else:
    front_flag = True

# print(front_flag, back_flag)

if front_flag or back_flag:
    print("Yes")
else:
    print("No")