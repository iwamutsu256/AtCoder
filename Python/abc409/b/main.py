N = int(input())
A = list(map(int,input().split()))
ans = 0
for i in range(0,101):
    count = 0
    for j in A:
        if j >= i:
            count += 1
    if count >= i:
        ans = i
print(ans)