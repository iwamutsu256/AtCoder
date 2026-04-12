N,M = map(int,input().split())
A = [int(x) for x in input().split()]
B = []
for i in range(1,N+1):
    if i not in A:
        B.append(i)
print(len(B))
for i in range(len(B)):
    if i < len(B)-1:
        print(B[i],end=" ")
    else:
        print(B[i],end = "")
print()