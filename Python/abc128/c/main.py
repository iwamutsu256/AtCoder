n,m = map(int,input().split())
switches = [list(map(int,input().split())) for _ in range(m)]

p = list(map(int,input().split()))

ans = 0

for i in range(2**n):
    bits = "0" + bin(i)[2:].zfill(n)
    # print(bits)
    on = 0
    for j in range(m):
        count = 0
        switch = switches[j]
        k = switch[0]
        for l in range(1,k+1):
            if bits[switch[l]] == "1":
                count += 1
        if count % 2 == p[j]:
            on += 1
    if on == m:
        ans += 1
print(ans)