N = int(input())
A = [0] + list(map(int,input().split()))
B = [0] + list(map(int,input().split()))
C = [0] + list(map(int,input().split()))

# 累積和の配列
SA = [0] * (N+1)
SB = [0] * (N+1)
SC = [0] * (N+1)
for i in range(1,N+1):
    SA[i] = SA[i-1] + A[i]
    SB[i] = SB[i-1] + B[i]
    SC[i] = SC[i-1] + C[i]

# yの最適位置の配列
good_Y = [N-1]*N
max_y = SB[N-1]-SB[0] + SC[N]-SC[N-1]
# iまでBに入る
for i in range(N-2,1,-1):
    if SB[i]-SB[0] + SC[N]-SC[i] > max_y:
        good_Y[i] = i
        max_y = SB[i]-SB[0] + SC[N]-SC[i]
    else:
        good_Y[i] = good_Y[i+1]

# print(good_Y)

# yが限られた中で最適をとるとき、xの最適を求める
max_x = SA[1] - SA[0] + SB[good_Y[2]] - SB[1] + SC[N] - SC[good_Y[2]]
for i in range(2,N-1):
    if SA[i] - SA[0] + SB[good_Y[i+1]] - SB[i] + SC[N] - SC[good_Y[i+1]] > max_x:
        max_x = SA[i] - SA[0] + SB[good_Y[i+1]] - SB[i] + SC[N] - SC[good_Y[i+1]]
        # print(f"x={i}, y={good_Y[i]}")
print(max_x)