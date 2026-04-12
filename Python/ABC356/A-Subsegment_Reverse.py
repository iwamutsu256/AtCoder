N,L,R = map(int,input().split())
for i in range(N):
    if L-1 < i+1 and i < R:
        print(R-(i-L+1),end = " ")
    else:
        print(i+1,end=" ")
print()