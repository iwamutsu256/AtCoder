from itertools import permutations
n = int(input())
p = tuple(map(int,input().split()))
q = tuple(map(int,input().split()))

nums = [int(x) for x in range(1,n+1)]

ps = permutations(nums,n)
ps = sorted(ps)
a = -1
b = -1
for i in range(len(ps)):
    if p == ps[i]:
        a = i
    if q == ps[i]:
        b = i
print(abs(a-b))