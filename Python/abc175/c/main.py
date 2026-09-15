x,k,d = map(int,input().split())

if x+k*d < 0 or x-k*d > 0:
    print(min(abs(x+k*d),abs(x-k*d)))
else:
    mv_cnt = abs(x) // d
    ans = abs(x) - d*mv_cnt
    if mv_cnt % 2 == k % 2:
        print(ans)
    else:
        print(abs(ans-d))