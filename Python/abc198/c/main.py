r,x,y = map(int,input().split())

# dist
dist = (x**2 + y**2)**0.5

ans = -(-dist//r)

print(int(ans))