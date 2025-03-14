N = int(input())
A = list(set(list(map(int,input().split()))))
A.sort()
print(A[-2])