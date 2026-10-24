q = int(input())
dic = dict()
current_id = 1

for _ in range(q):
    s = input()
    if s in dic.keys():
        print(dic[s])
    else:
        dic[s] = current_id
        print(current_id)
        current_id += 1