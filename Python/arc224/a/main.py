t = int(input())
for _ in range(t):
    k = int(input())
    # こたえは必ず100以下になるので、単純なループで探せる
    # どこかで0が2連続で含まれるかどうかを高速で見つける
    l = 0
    for i in range(101):
        l += k
        if '00' in str(l):
            print(l)
            break
