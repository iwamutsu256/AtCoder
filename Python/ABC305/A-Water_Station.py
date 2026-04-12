N = int(input())
if N % 5 == 0:
    print(N)
elif N % 5 == 1:
    print(N - 1)
elif N % 5 == 2:
    print(N - 2)
elif N % 5 == 3:
    print(N + 2)
else:
    print(N + 1)
