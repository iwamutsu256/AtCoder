X,Y,L,R,A,B = map(int,input().split())
ans = 0
for i in range(A,B):
    if L <= i and i < R:
        ans += X
    else:
        ans += Y
print(ans)