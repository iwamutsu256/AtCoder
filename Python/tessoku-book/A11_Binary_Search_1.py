N,X = map(int,input().split())
A = [int(x) for x in input().split()]
L = 0
R = N-1
answer = -1
while answer < 0:
    center = int((L+R)/2)
    if A[center] == X:
        answer = center
    elif A[center] > X:
        R = center - 1
    elif A[center] < X:
        L = center + 1
print(answer+1)