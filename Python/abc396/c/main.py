N,M = map(int,input().split())
B = list(map(int,input().split()))
W = list(map(int,input().split()))
B.sort(reverse=True)
W.sort(reverse=True)
#print(B,W)
length = min(len(B),len(W))
i = 0
count = 0
while i < length:
    if B[i] <= 0 and W[i] + B[i] > 0:
        count += B[i]+W[i]
        i += 1
    elif W[i] > 0 and W[i] + B[i] > 0: 
        count += B[i]+W[i]
        i += 1
    else:
        break
while i < len(B):
    if B[i] > 0:
        count += B[i]
        i += 1
    else:
        break
print(count)