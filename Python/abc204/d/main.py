import bisect

n = int(input())
t = list(map(int,input().split()))

candidates = set()

for i in range(n):
    if candidates:
        s = list(candidates)
        for j in s:
            candidates.add(j+t[i])
    candidates.add(t[i])

candidates = sorted(list(candidates))
idx = bisect.bisect_left(candidates,sum(t)/2)

print(candidates[idx])
