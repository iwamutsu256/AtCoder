import sys
sys.setrecursionlimit(10**7)

X1,X2,X3 = map(int,input().split())
def fact(n):
    if n == 0:
        return 1
    else:
        return (fact(n-1)*n)%998244353
# すべての組合せ
all = fact(X1+X2+X3) // (fact(X1)*fact(X2)*fact(X3))%998244353
# １と３が隣り合うとき
onethree = 2*fact(X1+X2+X3-1) // (fact(X1-1)*fact(X2)*fact(X3-1))%998244353
print((all-onethree)%998244353)