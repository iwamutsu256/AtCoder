def f(num):
    #1 x=R
    mx = 0
    for i in range(1,len(num)):
        mx = max(mx,int(num[i]))
    if int(num[0]) > mx:
        x1 = 1
    else:
        x1 = 0
    #2 n桁のうち上からk桁がRと一致
    x2 = 0
    for k in range(1,len(num)):
        mx = 0
        for i in range(1,k):
            mx = max(mx,int(num[i]))
        if int(num[0]) > mx:
            x2 += min(int(num[0]),int(num[k]))*(int(num[0])**(len(num)-(k+1)))
        else:
            x2 += 0
    #3 n桁で上から1桁目がD1より小さい
    x3 = 0
    for i in range(1,int(num[0])):
        x3 += i**(len(num)-1)
    #4 k+1桁
    x4 = 0
    for k in range(1,len(num)):
        for i in range(1,10):
            x4 += i**(k-1)
    #合計
    return x1+x2+x3+x4
L,R = input().split()
print(f(R)-f(str(int(L)-1)))