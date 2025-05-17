N = int(input())
P = list(map(int,input().split()))
A = []
B = []
ans = 0
# Aに極値となるインデックスを入れる
for i in range(N-1):
    if i == 0:
        if P[1] > P[0]:
            A.append(i)
    elif (P[i] < P[i+1] and P[i] < P[i-1]) or (P[i] > P[i+1] and P[i] > P[i-1]):
        A.append(i)
A.append(N-1)
for i in range(len(A)//2):
    B.append(A[2*i+1]-A[2*i])
if len(B) >= 2:
    for i in range(len(B)-1):
        ans += B[i]*B[i+1]
print(ans)
