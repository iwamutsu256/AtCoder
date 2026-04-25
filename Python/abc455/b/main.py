H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
count = 0
for h1 in range(H):
    for h2 in range(h1,H):
        for w1 in range(W):
            for w2 in range(w1,W):
                flag = True
                for i in range(h1,h2+1):
                    if not flag:
                        break
                    for j in range(w1,w2+1):
                        if S[i][j] != S[h1+h2-i][w1+w2-j]:
                            flag = False
                if flag:
                    count += 1
print(count)