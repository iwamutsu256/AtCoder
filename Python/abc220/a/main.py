A,B,C = map(int,input().split())
count = 0
while True:
    if count * C > 1000:
        print(-1)
        break
    if A <= count * C and count * C <= B:
        print(count * C)
        break
    count += 1