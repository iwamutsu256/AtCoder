n,m = map(int,input().split())
color = [-1 for _ in range(m)]
for i in range(n):
    c, s = map(int,input().split())
    color[c-1] = max(color[c-1],s)
print(" ".join(list(map(str,color))))