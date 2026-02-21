N,M = map(int,input().split())
is_buy = [False] * M
for i in range(N):
    L = int(input())
    X = list(map(int,input().split()))
    for j in range(len(X)):
        if not is_buy[X[j]-1]:
            is_buy[X[j]-1] = True
            print(X[j])
            break
    else:
        print(0)
