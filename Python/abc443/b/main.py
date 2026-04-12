N,K = map(int,input().split())
count = 0
beans = 0
while True:
    beans += N+count
    if beans >= K:
        break
    count += 1
print(count)