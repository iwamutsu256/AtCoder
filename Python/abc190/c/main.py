n,m = map(int,input().split())
needs = [list(map(int,input().split())) for _ in range(m)]
k = int(input())
persons = [list(map(int,input().split())) for _ in range(k)]

ans = 0
for i in range(2**k):
    selects = bin(i)[2:].zfill(k)
    # print(selects)
    bowls = [False for _ in range(n)]
    # print(selects)
    for j in range(len(selects)):
        # print(persons[j][int(selects[j])])
        bowls[persons[j][int(selects[j])]-1] = True
    count = 0
    for j in range(m):
        if bowls[needs[j][0]-1] and bowls[needs[j][1]-1]:
            count += 1
    # print(bowls,count)
    ans = max(ans,count)
print(ans)