T = int(input())
for _ in range(T):
    X,Y,K = map(int,input().split())
    count = 0
    while X != Y:
        if X > Y:
            X //= K
        else:
            Y //= K
        count += 1
    print(count)