n,q = map(int,input().split())
p = list(map(int,input().split()))
a = dict()
top = -1
last = -1
if n == 1:
    for i in range(q):
        _ = int(input())
    print(1)
    exit()
for i in range(n):
    if i == 0:
        a[p[i]] = [-1,p[i+1]]
        top = p[i]
    elif i == n-1:
        a[p[i]] = [p[i-1],-1]
        last = p[i]
    else:
        a[p[i]] = [p[i-1],p[i+1]]
# print(a)
for i in range(q):
    e = int(input())
    prev,next = a[e]
    if next != -1:
        if prev != -1:
            a[prev] = [a[prev][0],next]
            a[next] = [prev,a[next][1]]
        else:
            a[next] = [-1,a[next][1]]
            top = next
        a[last] = [a[last][0],e]
        a[e] = [last,-1]
        last = e
    # print(a)
# print(a)
current = top
for i in range(n):
    if i != n-1:
        print(current, end = " ")
    else:
        print(current)
    current = a[current][1]