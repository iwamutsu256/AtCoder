def sam(N):
    x = (N % 100000) // 10000
    a = (N % 10000) // 1000
    b = (N % 1000) // 100
    c = (N % 100) // 10
    d = (N % 10) // 1
    return int(a+b+c+d+x)

N,A,B = map(int,input().split())
sum = 0
for i in range(1,N+1):
    if A <= sam(i) and sam(i) <= B:
        sum += i
print(sum)