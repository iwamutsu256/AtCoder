n = int(input())
x = list(map(int,input().split()))
if max(x) < 0:
    print("Yes")
else:
    print("No")