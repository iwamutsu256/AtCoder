N,R = map(int,input().split())
for i in range(N):
    D,A = map(int,input().split())
    if D == 1 and 1600 <= R and 2799 >= R:
        R += A
    elif D == 2 and 1200 <= R and 2399 >= R:
        R += A
    else:
        pass
print(R)