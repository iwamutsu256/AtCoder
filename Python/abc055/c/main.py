import sys

n,m = map(int,input().split())
if n >= m//2:
    print(m//2)
    sys.exit()

count = n
m -= 2*n
print(n+m//4)