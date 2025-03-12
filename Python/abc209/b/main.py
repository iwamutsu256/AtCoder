N,X = map(int,input().split())
A = list(map(int,input().split()))
sam = 0
for i in range(N):
    if i % 2 == 1:
        sam += A[i]-1
    else:
        sam += A[i]
if X >= sam:
    print("Yes")
else:
    print("No")