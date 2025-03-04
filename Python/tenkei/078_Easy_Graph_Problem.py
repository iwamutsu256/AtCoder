N,M = map(int,input().split())
hen = [[] for _ in range(N)]
for i in range(M):
    a,b,= map(int,input().split())
    hen[a-1].append(b)
    hen[b-1].append(a)
ans = 0
for i in range(N):
    count = 0
    for j in range(len(hen[i])):
        if hen[i][j] < i+1:
            count += 1
    if count == 1:
        ans += 1
print(ans)