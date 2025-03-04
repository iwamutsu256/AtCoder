N,M,P = map(int,input().split())
count = 0
for i in range(N):
    if i + 1 >= M and (i + 1 - M) % P == 0:
        count += 1
print(count)