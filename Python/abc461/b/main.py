N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
flag = True
for i in range(N):
    if i != B[A[i]-1]-1:
        flag = False
if flag:
    print("Yes")
else:
    print("No")