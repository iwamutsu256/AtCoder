def connect_a_to_b(a,b):
    A = a-1
    B = b-1
    is_connect_list[A][B] = True
    start_list = []
    goal_list = []
    for i in range(N):
        if is_connect_list[i][A]:
            start_list.append(i)
        if is_connect_list[B][i]:
            goal_list.append(i)
    if not (start_list == [] and goal_list == []) and (start_list == [] or goal_list == []):
        if start_list == []:
            start_list.append(A)
        else:
            goal_list.append(B)
    for i in start_list:
        for j in goal_list:
            is_connect_list[i][j] = True
    return

N,M = map(int,input().split())
is_connect_list =[[False for _ in range(N)] for _ in range(N)]
for i in range(M):
    X,Y = map(int,input().split())
    connect_a_to_b(X,Y)
# print(is_connect_list)
Q = int(input())
is_black_connect_set = set()
for i in range(Q):
    num, v = map(int,input().split())
    if num == 1:
        for j in range(N):
            if is_connect_list[j][v-1]:
                is_black_connect_set.add(j+1)
    else:
        if v in is_black_connect_set:
            print("Yes")
        else:
            print("No")
