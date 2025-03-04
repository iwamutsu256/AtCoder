#差分の累積和
D = int(input())
N = int(input())
#累積和記録用の配列
#最終日まで出席する場合は最終日+1日目に-1されるので、配列の長さがD+1になっている
B = [int(0) for _ in range(D+1)]
#print(B)
for i in range(N):
    L,R = map(int,input().split())
    B[L-1] += 1
    B[R] -= 1
sum = 0
for i in range(D):
    sum += B[i]
    print(sum)
#print(B)