n = int(input())
a = list(map(int,input().split()))
count = 0
for i in range(0,n-2):
    if a[i] < a[i+1] and a[i+1] > a[i+2]:
        count += 1
print(count)