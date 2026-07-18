t = int(input())
for _ in range(t):
    px, py, qx, qy, rx, ry, sx, sy = map(int,input().split())
    dx1 = px-qx
    dy1 = py-qy
    dx2 = rx-sx
    dy2 = ry-sy
    cx1 = (px+qx)/2
    cy1 = (py+qy)/2
    cx2 = (rx+sx)/2
    cy2 = (ry+sy)/2
    if dx1*dy2 != dx2*dy1:
        print("Yes")
    elif dy1*(cy1-cy2) == -1*dx1*(cx1-cx2):
        print("Yes")
    else:
        print("No")