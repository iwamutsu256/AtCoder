def check(num):
    sum = 0
    for i in range(len(A)):
        if A[i] < num:
            sum += (num-A[i]+i)//(i+1)
    if sum <= K:
        return True
    else:
        return False


N,K = map(int,input().split())
A = list(map(int,input().split()))
ok = 1
ng = 10**20
while (ng-ok>1):
    middle = (ok+ng)//2
    if check(middle):
        ok = middle
    else:
        ng = middle
print(ok)