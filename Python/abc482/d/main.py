n = int(input())
x = list(map(int,input().split()))

# x = list(accumulate(x))

for i in range(n):
    if i == 0 or i == n-1:
        print((x[n-1]-x[0])//2)
    else:
        # 長いほうを調べる
        d1 = x[i] - x[0]
        d2 = x[n-1] - x[i]
        # 長いほうを先にやる
        # 距離が同じだったら近いほうが先
        d1_time = 0
        d2_time = 0
        d3 = x[i] - x[i-1]
        d4 = x[i+1] - x[i]
        d1_time = d1//2
        d3_time = d3//2
        d2_time = d3_time + d2//2
        d5_time = max(d1_time,d2_time)
        d2_time = d2//2
        d4_time = d4//2
        d1_time = d4_time + d1//2
        d6_time = max(d1_time,d2_time)
        print(min(d5_time,d6_time))
        # if d1 > d2:
        #     d1_time = d1//2
        #     d3_time = d3//2
        #     d2_time = d3_time + d2//2
        #     d5_time = max(d1_time,d2_time)
        # elif d1 < d2:
        #     d2_time = d2//2
        #     d4_time = d4//2
        #     d1_time = d4_time + d1//2
        #     d6_time = max(d1_time,d2_time)
        # elif d3 <= d4:
        #     d1_time = d1//2
        #     d3_time = d3//2
        #     d2_time = d3_time + d2//2
        # else:
        #     d2_time = d2//2
        #     d4_time = d4//2
        #     d1_time = d4_time + d1//2
        # print(max(d1_time,d2_time))