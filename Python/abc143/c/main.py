N = int(input())
S = list(input())
now = None
count = 0
for i in range(N):
    if S[i] != now:
        count += 1
        now = S[i]
print(count)