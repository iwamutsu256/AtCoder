N,T = map(int,input().split())
A = list(map(int,input().split()))
count = 0
before_time = 0
for i in range(N):
    if i == 0:
        count += 100
        before_time = A[i]
    elif A[i] - before_time < 100:
        pass
    else:
        if T - A[i] >= 100:
            count += 100
        else:
            count += T - A[i]
        before_time = A[i]

print(T-count)