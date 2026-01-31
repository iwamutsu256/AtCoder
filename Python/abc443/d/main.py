T = int(input())
for _ in range(T):
    N = int(input())
    R = list(map(int,input().split()))
    count = 0
    for i in range(1,N):
        if R[i] - R[i-1] > 1:
            count += R[i] - R[i-1] - 1
            R[i] = R[i-1] + 1
    for i in range(N-2,-1,-1):
        if R[i] - R[i+1] > 1:
            count += R[i] - R[i+1] - 1
            R[i] = R[i+1] + 1
    print(count)