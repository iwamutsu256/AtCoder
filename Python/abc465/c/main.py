from collections import deque

N = int(input())
S = list(input())
ans = deque([])
flag = False
for i in range(N):
    if flag:
        ans.appendleft(str(i+1))
    else:
        ans.append(str(i+1))
    if S[i] == "o":
        flag = not flag
if flag:
    ans = reversed(ans)
print(" ".join(ans))