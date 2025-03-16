import random
N, L = map(int, input().split())
T = list(map(int, input().split()))

for i in range(N):
    a = (i + 1) % N
    b = (i + 2) % N
    print(a, b)