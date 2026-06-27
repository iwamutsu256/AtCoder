N,M = map(int,input().split())
# iro = [1 for _ in range(N)]
birds = [list(map(int,input().split())) for _ in range(N)]
#  D日目でソート
birds.sort(key=lambda x:x[1])
iro = [0 for _ in range(N+1)]
count = 0
for i in range(N):
    if iro[birds[i][0]] == 0:
        count += 1
    iro[birds[i][0]] += 1

bird_index = 0

# M日間シミュレート
for i in range(1,M+1):
    while bird_index < N and birds[bird_index][1] == i:
        if iro[birds[bird_index][0]] == 1:
            count -= 1
        iro[birds[bird_index][0]] -= 1
        if iro[birds[bird_index][2]] == 0:
            count += 1
        iro[birds[bird_index][2]] += 1
        bird_index += 1
    # print(iro)
    print(count)