N,K,H,T,D = map(int,input().split())
color_own = [list(map(float,input().split())) for _ in range(K)]
color_target = [list(map(float,input().split())) for _ in range(H)]
v = [["1" for _ in range(N-1)] for _ in range(N)]
h = [["1" for _ in range(N)] for _ in range(N-1)]
for item in v:
    print(" ".join(item))
for item in h:
    print(" ".join(item))
for i in range(H):
    score = 100000000000000000
    num = -1
    for j in range(K):
        new_score = (color_target[i][0]-color_own[j][0])**2+(color_target[i][1]-color_own[j][0])**2+(color_target[i][0]-color_own[j][0])**2
        if new_score <= score:
            score = new_score
            num = j+1
    print(f"1 1 1 {num}")
    print("2 1 1")