n,v = map(int,input().split())
w = list(map(int,input().split()))

ans = 0

for i in range(n-2):
    for j in range(i+1,n-1):
        for k in range(j+1,n):
            if i+j+k+3 <= v:
                ans = max(ans,w[i]+w[j]+w[k])
print(ans)