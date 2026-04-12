N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
A.sort(reverse=True)
B.sort(reverse=True)
X = 0
for i in range(N):
    if X == 0:
        if i != N-1:
            if A[i] <= B[i]:
                pass
            else:
                X = A[i]
        else:
            X = A[i]
    else:
        if A[i] <= B[i-1]:
            pass
        else:
            print(-1)
            break
else:
    print(X)