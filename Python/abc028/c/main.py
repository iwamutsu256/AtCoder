from itertools import combinations
a = list(map(int,input().split()))

sums = set()
for t in combinations(a,3):
    sums.add(sum(t))
sums = sorted(list(sums))
print(sums[-3])