import math
T = int(input())
L,X,Y = map(int,input().split())
Q = int(input())
for i in range(Q):
    E = int(input())
    x = (L/2)*(1-math.cos(2*math.pi*E/T))
    y = math.sqrt(X**2+(-1*(L/2)*math.sin(2*math.pi*E/T)-Y)**2)
    print(math.atan(x/y)*360/(2*math.pi))