import bisect
N,Q = map(int,input().split())
A = list(map(int,input().split()))
A.sort()
for _ in range(Q):
    x,y = map(int,input().split())
    # Xが入る場所と,X+Yが入る場所を求める。
    # その間にあるリストに含まれる数の個数(挿入するリストのインデックスの差)から
    # X+Yにプラスする分を求め、その分をずらす
    start = bisect.bisect_right(A,x)
    end = bisect.bisect_right(A,x+y)
    count = 0
    while end > start:
        count += end - start
        start = end
        end = bisect.bisect_right(A, x + y + count)
    if start == 0:
        print(x + y + count)
    else:
        print(A[start-1] + y + count)