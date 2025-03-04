N = int(input())
S = input()
A = [S.index("A"),S.index("B"),S.index("C")]
A.sort()
print(A[-1]+1)
