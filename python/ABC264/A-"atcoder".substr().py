L,R = map(int,input().split())
A = "atcoder"
for i in range(R-L+1):
    print(A[L+i-1],end="")
print()