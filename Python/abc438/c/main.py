from collections import deque

# s = deque([])

N = int(input())
A = list(map(int,input().split()))
B = deque([])

for i in range(N):
    B.append(A[i])
    if len(B) > 3 and B[-1] == B[-2] == B[-3] == B[-4]:
        B.pop()
        B.pop()
        B.pop()
        B.pop()
print(len(B))