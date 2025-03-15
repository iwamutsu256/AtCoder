from collections import deque
N,K = map(int,input().split())
A = deque(list(map(str,input().split())))
for i in range(K):
    A.popleft()
    A.append("0")
print(" ".join(A))