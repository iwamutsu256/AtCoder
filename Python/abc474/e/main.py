t = int(input())
for _ in range(t):
    n = int(input())
    a_list = []
    b_list = []
    goods = []
    a_min = 10**9 + 1
    for i in range(n):
        a,b = map(int,input().split())
        a_min = min(a,a_min)
        goods.append([a,b,a-b])
        a_list.append(a)
        b_list.append(b)
    goods.sort(key=lambda x:x[2], reverse=True)
    # print(goods)
    cost = sum(a_list)
    discount_count = 0
    # print(cost)
    for i in range(n):
        if discount_count < n//2:
            cost -= goods[i][0] - goods[i][1]
            # print(f"{i}番目: coupon使った, 割引:{goods[i][0] - goods[i][1]}")
            discount_count += 1
        else:
            if n % 2 == 1 and discount_count == n//2:
                if goods[i][0] > a_min + goods[i][1]:
                    cost -= goods[i][0] - goods[i][1] - a_min
                    discount_count += 1
            else:
                if goods[i][0] > a_min*2 + goods[i][1]:
                    cost -= goods[i][0] - goods[i][1] - a_min*2
                    # print(f"{i}番目: coupon使った, 割引:{goods[i][0] - goods[i][1] - a_min}")
                    discount_count += 1
                else:
                    pass
                    # print(f"{i}番目: coupon使ってない")
    print(cost)