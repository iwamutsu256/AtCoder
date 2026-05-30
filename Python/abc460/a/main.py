N,M = map(int,input().split())
count = 0
while M != 0:
    M = N % M
    count += 1
print(count)