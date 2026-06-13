T = int(input())
for _ in range(T):
    A,B,X,Y = map(int,input().split())
    X,Y = abs(X),abs(Y)
    # (min(X,Y),min(X,Y))までのコスト
    cost = 2*min(X,Y)*min(A,B)
    dist = max(X,Y) - min(X,Y)
    # 最短移動でコストBの時
    if X<Y:
        A_count = dist // 2
        B_count = A_count if dist % 2 == 0 else A_count+1
    else:
        B_count = dist // 2
        A_count = B_count if dist % 2 == 0 else B_count+1
    if A > B and 3*B < A:
        B_count += 3*A_count
        A_count = 0
    elif A < B and 3*A < B:
        A_count += B_count*3
        B_count = 0
    cost += A_count * A + B_count * B
    print(cost)