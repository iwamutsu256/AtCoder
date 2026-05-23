X = int(input())
S = list("HelloWorld")
T = S[:X-1] + S[X:]
print("".join(T))