N,K = map(int,input().split())
A = list(map(int,input().split()))
dict = dict()
for i in A:
    if i in dict:
        dict[i] += 1
    else:
        dict[i] = 1
list = []
for key, value in dict.items():
    list.append(key*value)
list.sort()
# print(list)
if len(list) <= K:
    print(0)
else:
    print(sum(list[:len(list)-K]))