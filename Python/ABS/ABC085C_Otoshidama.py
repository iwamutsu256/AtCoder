N,Y = map(int,input().split())
#a+b+c = N より、c = N-(a+b)なので、aとbの二重forループによる全探索
ans = [-1,-1,-1]
for i in range(N+1):
    for j in range(N-i+1):
        if N-(i+j) >= 0 and i*10000+j*5000+1000*(N-(i+j)) == Y:
            ans = [i,j,N-(i+j)]
print(ans[0],ans[1],ans[2])
