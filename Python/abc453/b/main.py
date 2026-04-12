T,X = map(int,input().split())
A = list(map(int,input().split()))
sensor = 0
for i in range(T+1):
    if i == 0:
        sensor = A[i]
        print(i,sensor)
    elif abs(A[i] - sensor) >= X:
        sensor = A[i]
        print(i,sensor)
