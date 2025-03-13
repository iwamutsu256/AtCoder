N = int(input())
A = list(map(int,input().split()))
B = [int(x)+1 for x in range(N)]
A.sort()
if A == B:
    print("Yes")
else:
    print("No")