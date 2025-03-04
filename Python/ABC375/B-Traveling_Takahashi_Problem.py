from math import sqrt


N = int(input())
oldx = 0
oldy = 0
sum = 0
for i in range(N+1):
    if i == N:
        newX,newY = 0,0
    else:
        newX,newY = map(float,input().split())
    d = sqrt(pow(oldx-newX,2)+pow(oldy-newY,2))
    oldx = newX
    oldy = newY
    sum += d
print(sum)