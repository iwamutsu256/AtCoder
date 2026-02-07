N,M = map(int,input().split())
birds = [[0,0] for _ in range(M)]
for _ in range(N):
    A,B = map(int,input().split())
    birds[A-1][0] += B
    birds[A-1][1] += 1
for bird in birds:
    print(bird[0]/bird[1])