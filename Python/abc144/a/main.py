A,B = map(int,input().split())
if max(A,B) >= 10:
    print(-1)
else:
    print(A*B)