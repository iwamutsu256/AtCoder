N = int(input())
C,B,A = sorted(map(int,input().split()))
L = 9999
ans = 9999
for i in range(min(L,N//A)+1):
    a = N - A*i
    for j in range(min(L,a//B)+1):
        b = a - B*j
        if b % C == 0:
            ans = min(ans,i+j+(b//C))
print(ans)
