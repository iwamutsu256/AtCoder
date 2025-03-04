def ink(i,j,str):
    global grid
    for k in range(j - i + 1):
        grid[i][i+k] = str
        grid[i+k][i] = str
        grid[j][i+k] = str
        grid[i+k][j] = str
    return

N = int(input())
grid = [["." for _ in range(N)] for _ in range(N)]
for i in range(N):
    j = N-i-1
    if i <= j:
        if i % 2 == 0:
            str = "#"
        else:
            str = "."
        ink(i,j,str)
#print(grid)

for i in range(N):
    print("".join(grid[i]))