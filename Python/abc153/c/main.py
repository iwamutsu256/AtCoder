N,K = map(int,input().split())
H = list(map(int,input().split()))
H.sort()
if len(H) <= K:
    print(0)
else:
    for i in range(K):
        H.pop()
    count = 0
    for i in range(len(H)):
        count += H.pop()
    print(count)