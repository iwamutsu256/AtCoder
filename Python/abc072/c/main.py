n = int(input())
a = list(map(int,input().split()))

sm = [0 for _ in range(10**5+3)]
for i in range(n):
    sm[a[i]] += 1
    sm[a[i]+3] -= 1

tm = [0 for _ in range(len(sm))]
for i in range(len(sm)):
    tm[i] = tm[i-1] + sm[i]
print(max(tm))