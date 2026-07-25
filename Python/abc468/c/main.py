import itertools
n = int(input())
p = list(map(int,input().split()))
q = list(map(int,input().split()))
num = [int(x) for x in range(1,n+1)]
count = 0
nums = list(map(list,itertools.permutations(num)))
for nu in nums:
    if p < nu and nu < q:
        count += 1

print(count)
