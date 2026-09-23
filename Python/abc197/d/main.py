import math

n = int(input())
x0, y0 = map(int,input().split())
x1,y1 = map(int,input().split())

cx,cy = (x0+x1)/2, (y0+y1)/2

theta = 360/n

x,y = x0-cx,y0-cy
sin = math.sin(math.radians(theta))
cos = math.cos(math.radians(theta))
x,y = x*math.cos(math.radians(theta)) - y*math.sin(math.radians(theta)),x*math.sin(math.radians(theta)) + y*math.cos(math.radians(theta))
x += cx
y += cy

print(x,y)