H,W = map(int,input().split())
mapping = [["." for _ in range(W)] for _ in range(H)]
for i in range(H):
    for j in range(W):
        if i == 0 or i == H-1 or j == 0 or j == W-1:
            mapping[i][j] = "#"
for i in range(H):
    print("".join(mapping[i]))