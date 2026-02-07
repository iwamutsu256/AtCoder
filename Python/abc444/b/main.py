N,K = map(int,input().split())
count = 0
for i in range(1,N+1):
    string = list(map(int,list(str(i))))
    cnt = 0
    for j in string:
        cnt += j
    if cnt == K:
        count += 1
print(count)