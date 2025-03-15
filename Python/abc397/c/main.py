from collections import Counter
N = int(input())
A = list(map(int,input().split()))
Count_B = Counter(A)
Count_A = dict()
countA = 0
countB = len(Count_B)
ans = 0
for i in range(N):
    if A[i] in Count_A:
        Count_A[A[i]] += 1
    else:
        Count_A[A[i]] = 1
        countA += 1
    Count_B[A[i]] -= 1
    if Count_B[A[i]] == 0:
        Count_B.pop(A[i])
        countB -= 1
    ans = max(ans,countA+countB)
print(ans)