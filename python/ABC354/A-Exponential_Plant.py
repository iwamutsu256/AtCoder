H = int(input())
n = 1
i = 1
while n <= H:
    n = 2**i - 1
    i += 1
print(i-1)