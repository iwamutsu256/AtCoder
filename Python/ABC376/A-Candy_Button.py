N ,C= map(int,input().split())
T = list(map(int,input().split()))
U = 0
sum = 0
for i in range(N):
    if T[i] - U >= C or i == 0:
        sum += 1
        U = T[i]
print(sum)
