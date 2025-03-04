N,K = map(int,input().split())
count = 0
for i in range(1,N+1):
    for j in range(1,N+1):
        if 1 <= K-(i+j) and K-(i+j) <= N:
            #print(i,j,K-(i+j))
            count += 1
print(count)