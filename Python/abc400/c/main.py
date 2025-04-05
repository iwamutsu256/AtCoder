import math

def count_odd(count):
    if count % 2 == 0:
        return count // 2
    else:
        return (count+1) // 2

def count_two(num,N):
    tmp = N // num
    count = math.isqrt(tmp)
    return count_odd(count)

N = int(input())
i = 1
count = 0
while 2 ** i <= N:
    count += count_two(2**i, N)
    i += 1
print(count)