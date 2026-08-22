n = int(input())
l = list(map(int,input().split()))
left = 0
right = sum(l)
score = right
for i in range(n):
    score = min(score,abs(right-left))
    left += l[i]
    right -= l[i]
print(score)