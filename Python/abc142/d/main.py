import math

a,b = map(int,input().split())


def factorization(n):
    """nを素因数分解
    2以上の整数n => [[素因数, 指数], ...]の2次元リスト
    1を入力すると、[[1,1]]が返却される"""
    # factorization(24) 

    ## [[2, 3], [3, 1]] 
    ##  24 = 2^3 * 3^1

    arr = []
    temp = n
    for i in range(2, int(-(-n**0.5//1))+1):
        if temp%i==0:
            cnt=0
            while temp%i==0:
                cnt+=1
                temp //= i
            arr.append([i, cnt])

    if temp!=1:
        arr.append([temp, 1])
    
    if arr==[]:
        arr.append([n, 1])
        
    return arr
    


c = math.gcd(a,b)
p = factorization(c)
if [1,1] in p:
    print(1)
else:
    print(len(p)+1)