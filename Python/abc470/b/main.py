n = int(input())
c = list(map(int,input().split()))
count = [0 for _ in range(n)]
for i in range(n):
    count[c[i]-1] += 1
print(n-max(count))