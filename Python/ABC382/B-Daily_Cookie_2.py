N,D = map(int,input().split())
S = input()
T = list(reversed(S))
for i in range(D):
    T[T.index("@")] = "."
T.reverse()
V = "".join(T)
print(V)