# 難易度がb
# すべてのフレーバーでb以下になる最大の数を足す
# それプラス1枚で確定勝利
import bisect
N,Q = map(int,input().split())
A = list(map(int,input().split()))
A.sort()
C = [0]*len(A)
for i in range(len(A)):
    if i == 0:
        C[i] = A[i]
    else:
        C[i] = C[i-1] + A[i]
for i in range(Q):
    B = int(input())
    num = bisect.bisect_left(A,B)
    if num == 0:
        ans = (B-1)*len(A) + 1
    else:
        ans = C[num-1] + (B-1)*(len(A)-num) + 1
    if ans <= C[-1]:
        print(ans)
    else:
        print(-1)