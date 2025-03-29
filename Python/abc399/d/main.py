T = int(input())
for i in range(T):
    N = int(input())
    A = list(map(int,input().split()))
    my_dict = dict()
    no = set()
    count = 0
    for i in range(2*N):
        # 1回目のを辞書に登録
        if A[i] not in my_dict:
            if i == 0:
                my_dict[A[i]] = {A[i+1]}
            else:
                my_dict[A[i]] = {A[i+1],A[i-1]}
            if i < 2*N-1:
                if A[i] == A[i+1]:
                    no.add(A[i])
        else:
            if i == 2*N-1:
                two = {A[i-1]}
            else:
                two = {A[i-1],A[i+1]}
            if A[i] not in no:
                count += len((my_dict[A[i]] & two) - no)
    print(count // 2)