from collections import Counter

n = int(input())
a = list(map(int,input().split()))

counter = Counter(a)

ans = sum(a)

q = int(input())

for _ in range(q):
    b,c = map(int,input().split())
    count_b = counter[b]
    ans += (c-b)*count_b
    counter[b] = 0
    if c in counter.keys():
        counter[c] += count_b
    else:
        counter[c] = count_b
    print(ans)