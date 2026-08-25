n,q = map(int,input().split())
a = [0 for _ in range(n+1)]
xor = 0
a_set = set()
for _ in range(q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        xor ^= a[query[1]]
        a[query[1]] += 1
        a_set.add(query[1])
        xor ^= a[query[1]]
    else:
        removing = set()
        for i in a_set:
            xor ^= a[i]
            a[i] -= 1
            if a[i] == 0:
                removing.add(i)
            xor ^= a[i]
        a_set -= removing
    print(xor)