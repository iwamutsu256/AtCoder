T = int(input())
for _ in range(T):
    N,H = map(int,input().split())
    maximum = H
    minimum = H
    flag = True
    before_T = 0
    for i in range(N):
        t,l,u = map(int,input().split())
        maximum += t - before_T
        minimum -= t - before_T
        if maximum < l or minimum > u:
            flag = False
        maximum = min(maximum,u)
        minimum = max(minimum,l)
        # print(minimum,maximum)
        before_T = t
    else:
        if flag:
            print("Yes")
        else:
            print("No")
