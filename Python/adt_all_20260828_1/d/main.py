from itertools import permutations
x = list(input())
ans = 10**6
for num in permutations(x,len(x)):
    # print(num)
    num = int("".join(num))
    if len(str(num)) == len(x):
        ans = min(ans,num)
print(ans)