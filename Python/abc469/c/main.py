n = int(input())
s = list(input())
# 累積和
sum = [0 for _ in range(n+1)]
for i in range(n):
    if s[i] == "o":
        sum[i+1] = sum[i]+1
    else:
        sum[i+1] = sum[i]
# print(sum)
for k in range(1,n+1):
    count = k
    index = k
    d = sum[k]
    while d > 0 and index < n:
        prev_index = index
        index = min(n,index+d)
        d = sum[index]-sum[prev_index]
    print(index)
