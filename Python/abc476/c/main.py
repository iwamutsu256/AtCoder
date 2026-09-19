n = int(input())
a = list(map(int,input().split()))

t = sorted(a[:3],reverse=True)
print(t[-1])
for i in range(3,n):
    t = sorted(t+[a[i]],reverse=True)
    t = t[:3]
    # print(t)
    print(t[-1])