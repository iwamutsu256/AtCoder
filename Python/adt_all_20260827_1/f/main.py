from collections import defaultdict
n,m = map(int,input().split())
dict = defaultdict(list)
for i in range(m):
    a,b = map(int,input().split())
    dict[a].append(b)
    dict[b].append(a)
ans = []
for i in range(1,n+1):
    rigai_count = len(dict[i])
    # print(rigai_count)
    kouho_count = n-rigai_count-1
    # print(kouho_count)
    if kouho_count >= 3:
        ans.append(kouho_count*(kouho_count-1)*(kouho_count-2)//6)
    else:
        ans.append(0)
print(*ans)