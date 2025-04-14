N,Q = map(int,input().split())
S = list(input())
current_count = 0
for i in range(N-2):
    if S[i] == "A" and S[i+1] == "B" and S[i+2] == "C":
        current_count += 1
for i in range(Q):
    X,C = input().split()
    X = int(X)
    before = 0
    after = 0
    for j in range(max(0,X-3),min(X,N-2)):
        if S[j] == "A" and S[j+1] == "B" and S[j+2] == "C":
            before += 1
    S[X-1] = C
    for j in range(max(0,X-3),min(X,N-2)):
        if S[j] == "A" and S[j+1] == "B" and S[j+2] == "C":
            after += 1
    delta = after - before
    current_count += delta
    print(current_count)