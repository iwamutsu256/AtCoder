X,Y,N = map(int,input().split())
A,B = 0,0
if X > Y/3:
    for i in range(N // 3):
        B += 3
    for i in range(N % 3):
        A += 1
else:
    for i in range(N):
        A += 1
print(A*X+(B//3)*Y)