N = int(input())
d = [0]*N
for i in range(N):
    d[i] = int(input())
e = list(set(d))
print(len(e))