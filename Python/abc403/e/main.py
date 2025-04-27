Q = int(input())
X = dict()
Y = dict()
ans = 0
for i in range(Q):
    T,S = input().split()
    T = int(T)
    S = list(S)
    if T == 1:
        count = 0
        for j in range(len(S)):
            if "".join(S[:j+1]) in Y:
                count += Y["".join(S[:j+1])]
        ans -= count
        if "".join(S) in X:
            X["".join(S)] += 1
        else:
            X["".join(S)] = 1
    else:
        for j in range(len(S)):
            if "".join(S[:j+1]) in X:
                break
        else:
            ans += 1
        if "".join(S) in Y:
            Y["".join(S)] += 1
        else:
            Y["".join(S)] = 1
    print(ans)