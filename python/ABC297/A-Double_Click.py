N,D = map(int,input().split())
T = [int(x) for x in input().split()]
time = -1
for i in range(1,N):
    if T[i] - T[i-1] <= D:
        time = T[i]
        break
print(time)