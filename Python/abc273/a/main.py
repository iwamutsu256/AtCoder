def function(N):
    if N == 0:
        return 1
    else:
        return function(N-1)*N

N = int(input())
print(function(N))