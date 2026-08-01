n,m = map(int,input().split())
final = [list(map(int,input().split())) for _ in range(m)]

small, big = final[0]
small_list = {int(i) for i in range(1,n+1)}
big_list = {int(i) for i in range(1,n+1)}
small_list.remove(small)
big_list.remove(big)
big_list.remove(small)
small_flag = True
big_flag = True
for i in range(m):
    a,b = final[i]
    # if i == 0:
    #     small_list.append(b)
    if small not in (a,b) and small_flag:
        small_flag = False
    if big not in (a,b) and big_flag:
        big_flag = False
    if small_flag and big_flag:
        pass
    elif small_flag:
        big_list = {a,b} & big_list
    elif big_flag:
        small_list = {a,b} & small_list
    elif small in (a,b):
        big_list = {a,b} & big_list
    elif big in (a,b):
        small_list = {a,b} & small_list
    else:
        small_list = {a,b} & small_list
        big_list = {a,b} & big_list
    # print(small_flag,big_flag)
    # print(small_list,big_list)
print(len(small_list)+len(big_list))