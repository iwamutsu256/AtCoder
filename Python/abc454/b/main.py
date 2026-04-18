N,M = map(int,input().split())
F = list(map(int,input().split()))
kind = len(list(set(F)))
if kind == N:
    print("Yes")
else:
    print("No")

if kind == M:
    print("Yes")
else:
    print("No")
