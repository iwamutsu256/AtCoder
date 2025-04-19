import math
import collections
N,M = map(int,input().split())
T = []
for i in range(M):
    A,B = map(int,input().split())
    pos_A_x = math.cos(2*A*math.pi/N)
    pos_A_y = math.sin(2*A*math.pi/N)
    pos_B_x = math.cos(2*B*math.pi/N)
    pos_B_y = math.sin(2*B*math.pi/N)
    if pos_B_x - pos_A_x == 0:
        theta = 90
    else:
        cos = 1 / (pos_B_x - pos_A_x)
        theta = round(math.degrees(math.acos(cos)), 9)
    T.append(theta)
count = collections.Counter(T)
counter = 0
for c in count:
    counter += count[c] * (count[c] - 1) // 2
print((M*(M-1)//2)-counter)