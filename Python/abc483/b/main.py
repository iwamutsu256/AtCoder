n,q = map(int,input().split())
k = list(map(int,input().split()))

card = [int(x) for x in range(1,n+1)]
flip = [0 for _ in range(n)]
# print(card)
for i in range(q):
    card[:k[i]] = reversed(card[:k[i]])
    for j in range(k[i]):
        flip[j] = (flip[j] + 1) % 2
    flip[:k[i]] = reversed(flip[:k[i]])
    # print(flip)
for i in range(n):
    if flip[i] == 0:
        print(card[i])
    else:
        print(-card[i])