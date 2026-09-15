from collections import Counter
n,k = map(int,input().split())
a = list(map(int,input().split()))
c = Counter(a)
d = c.most_common()
ans = 0
for i in range(len(d)-k):
    ans += d[len(d)-1-i][1]
print(ans)