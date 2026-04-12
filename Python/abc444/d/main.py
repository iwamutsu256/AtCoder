N = int(input())
A = list(map(int,input().split()))
B = [0] * (max(A))
# print(B)
for i in range(N):
    B[A[i]-1] += 1
for i in range(len(B)-1):
    B[len(B)-2-i] += B[len(B)-1-i]
# print(B)
S = 0
for i in range(len(B)):
    B[i] += S
    S = B[i] // 10
    B[i] = B[i] % 10
B.reverse()
if S != 0:
    S = str(S)
else:
    S = ""
print(S + "".join(map(str,B)))