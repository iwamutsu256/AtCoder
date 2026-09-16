from collections import Counter

n = int(input())
a = list(map(int,input().split()))

counter = Counter(a)

k = 0

for v in counter.values():
    if v >= 2:
        k += v*(v-1)//2

for i in range(n):
    old_v = counter[a[i]]
    old_k = old_v*(old_v - 1)//2 if old_v >= 2 else 0
    if old_k == 0:
        print(k)
        continue

    new_v = old_v - 1
    new_k = new_v*(new_v-1)//2 if new_v >= 2 else 0

    diff = old_k - new_k

    print(k-diff)