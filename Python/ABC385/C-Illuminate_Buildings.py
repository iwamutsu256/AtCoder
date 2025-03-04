def check(ans):
    counter = 0
    for i in range(ans):
        height = 0
        for j in H[i::ans]:
            if height != j:
                current = 0
                height = j
            current += 1
            counter = max(counter,current) 
    return counter
    
N = int(input())
H = list(input().split())
count = 1
for i in range(N):
    if check(i) > count:
        count = check(i)
print(count)