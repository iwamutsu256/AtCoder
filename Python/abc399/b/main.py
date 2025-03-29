N = int(input())
P = list(map(int,input().split()))
Q = [0]* N
count = 1
for i in range(100,0,-1):
    point = i
    counter = 0
    for j in range(N):
        if P[j] == point:
            Q[j] = count
            counter += 1
    count += counter
for i in range(N):
    print(Q[i])