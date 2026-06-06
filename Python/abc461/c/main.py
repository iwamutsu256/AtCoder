N,K,M = map(int,input().split())
J = [list(map(int,input().split())) for _ in range(N)]
J.sort(key=lambda x: x[1])
kind = set()
ans = 0
extra = []
for i in range(M):
    [c,v] = J.pop()
    if c in kind:
        while c in kind:
            extra.append([c,v])
            [c,v] = J.pop()
    ans += v
    kind.add(c)
J = J + extra
# print(J)
J.sort(key=lambda x: x[1])
for i in range(K-M):
    [c,v] = J.pop()
    ans += v
# print(J,extra)
# print(ans,extra)
# if K-M <= len(extra):
#     ans += sum(extra[:K-M])
# else:
#     ans += sum(extra)
#     for i in range(K-M-len(extra)):
#         [c,v] = J.pop()
#         ans += v

print(ans)