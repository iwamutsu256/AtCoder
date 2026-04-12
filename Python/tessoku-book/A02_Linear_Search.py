N,X = map(int,input().split())
A = [int(x) for x in input().split()]
answer = False
for i in range(N):
    if A[i] == X:
        answer = True
if answer:
    print("Yes")
else:
    print("No")
