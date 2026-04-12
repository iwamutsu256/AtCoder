S = list(map(int,list(input())))
counter = []
numbers = []
cnt = 0
num = -1
for i in range(len(S)):
    if i == 0:
        cnt = 1
        num = S[i]
    elif S[i] != S[i-1]:
        counter.append(cnt)
        numbers.append(num)
        cnt = 1
        num = S[i]
    else:
        cnt += 1
counter.append(cnt)
numbers.append(num)
# print(counter)
# print(numbers)
ans = 0
for i in range(1,len(numbers)):
    if numbers[i] == numbers[i-1] + 1:
        ans += min(counter[i],counter[i-1])
print(ans)