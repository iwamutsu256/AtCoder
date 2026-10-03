n,m = map(int,input().split())

small = m//n

p = m%n

for i in range(1,n+1):
    if i <= p:
        print(small+1)
    else:
        print(small)