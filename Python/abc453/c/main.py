N = int(input())
L = list(map(int,input().split()))
# 全探索
ans = 0
for i in range(2**N):
    bit = bin(i)[2:].zfill(N)
    count = 0
    current = 0.5
    for j in range(N):
        if bit[j] == "1":
            # 正の方向
            # if current * (current + L[j]) < 0:
            if current < 0 and current + L[j] > 0:
                count += 1
            current += L[j]
        else:
            # if current * (current - L[j]) < 0:
            if current > 0 and current - L[j] < 0:
                count += 1
            current -= L[j]
    ans = max(ans,count)
print(ans)