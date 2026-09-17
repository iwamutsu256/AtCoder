n = int(input())
h = list(map(int,input().split()))

grid = [[False for _ in range(100)] for _ in range(n)]

for i in range(n):
    for j in range(100):
        if h[i] > j:
            grid[i][j] = True

# print(grid)

ans = 0
for j in range(100):
    count = 0
    now = False
    for i in range(n):
        if (now == True and grid[i][j] != now) or (i == n-1 and grid[i][j] == True):
            count += 1
        now = grid[i][j]
    # print(f"now: {j}, {count}")
    ans += count
print(ans)