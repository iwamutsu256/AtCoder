import math
A,B = map(int,input().split())
num = math.floor(A/B)
if abs((A/B) - num) <= 0.5:
    print(num)
else:
    print(num + 1)