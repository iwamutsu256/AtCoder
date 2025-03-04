N,K = map(int,input().split())
A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
C = [int(x) for x in input().split()]
D = [int(x) for x in input().split()]
E = [0]*(N**2)
F = [0]*(N**2)
for i in range(N):
    for j in range(N):
        E[N*i+j] = A[i]+B[j]
        F[N*i+j] = C[i]+D[j]
E.sort()
F.sort()
answer = False
for i in range(N**2):
    find = K-E[i]
    L = 0
    R = N**2 - 1
    while L <= R:
        center = (L+R) // 2
        #print(center)
        if F[center] < find:
            L = center + 1
        if F[center] > find:
            R = center - 1
        if F[center] == find:
            answer = True
            break
    if L == R:
        answer = True
if answer:
    print("Yes")
else:
    print("No")