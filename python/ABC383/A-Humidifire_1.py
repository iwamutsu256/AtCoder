N = int(input())
T = 0
V = 0
for i in range(N):
    T2,V2 = map(int,input().split())
    V -= T2 - T
    if V < 0:
        V = 0
    V += V2
    T = T2
print(V)
