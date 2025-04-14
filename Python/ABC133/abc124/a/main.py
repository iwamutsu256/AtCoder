A,B = map(int,input().split())
X = 0
for _ in range(2):
    if A > B:
        X += A
        A -= 1
    else:
        X += B
        B -= 1
print(X)