import bisect

n,k,t = map(int,input().split())
a = list(map(int,input().split()))

a.sort()

compleated = 0
push = 0
for i in range(n):
    space_time = min(a[i],t) - compleated
    if space_time < 0:
        space_time = 0
    push += -(-space_time//k)
    compleated = a[i] + k
    if compleated >= t:
        break
else:
    space_time = t - compleated
    if space_time < 0:
        space_time = 0
    push += -(-space_time//k)
    compleated = t + k
print(push)