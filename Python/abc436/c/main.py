def set_block(x,y):
    for i in range(-1,2):
        for j in range(-1,2):
            if 0 <= x+i < N and 0 <= y+j < N:
                Block_list.add((x+i,y+j))
    return

N,M = map(int,input().split())
Block_list = set()
count = 0
for i in range(M):
    x,y = map(int,input().split())
    if (x-1,y-1) not in Block_list:
        set_block(x-1,y-1)
        count += 1
print(count)