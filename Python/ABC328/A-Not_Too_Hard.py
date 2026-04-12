N,X = map(int,input().split())
S = [int(x) for x in input().split()]
count = 0
for i in range(len(S)):
    if S[i] <= X:
        count += S[i]
print(count)