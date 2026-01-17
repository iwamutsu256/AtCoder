N,K,X = map(int,input().split())
A = list(map(int,input().split()))
A.sort()
A = A[:K]
count = 0
volume = 0
while volume < X:
    if count == K:
        print(-1)
        break
    volume += A[-1 -count]
    count += 1
else:
    if count + N - K <= N:
        print(count + N - K)
    else:
        print(-1)
