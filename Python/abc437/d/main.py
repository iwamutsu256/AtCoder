# Aをソートして累積和を作成
# Bから一個ずつ取り出す
# 2分探で絶対値の外す場所を探す
# 累積和にて計算
import bisect
N,M = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
A = sorted(A)
A_sum = [0]
# 累積和
for i in range(1,N+1):
    A_sum.append(A_sum[i-1] + A[i-1])
ans = 0
for i in range(M):
    num = bisect.bisect_left(A,B[i])
    ans += (-A_sum[num]+B[i]*num+(A_sum[N]-A_sum[num])-B[i]*(N-num)) #% 998244353
    ans = ans % 998244353
print(ans)