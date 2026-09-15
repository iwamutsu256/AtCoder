r,x,y = map(int,input().split())

# dist
dist = (x**2 + y**2)**0.5
if dist < r:
    print(2)
elif dist == r:
    print(1)
else:
    ans = -(-dist//r)
    print(int(ans))