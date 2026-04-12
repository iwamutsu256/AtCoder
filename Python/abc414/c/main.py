import math

def base_n(num_10, n):
    str_n = ""
    while num_10:
        if num_10%n >= 10:
            return -1
        str_n += str(num_10 % n)
        num_10 //= n
    return int(str_n[::-1])

def is_palindrome(n):
    n = str(n)
    return n == n[::-1]

A = int(input())
N = int(input())
ans = 0
keta = len(str(N))

# 先頭x桁を決めて回文を構築し、N以下かつA進数でも回文か判定
for i in range(1, keta+1):
    x = (i + 1) // 2
    start = 10**(x-1) if x > 1 else 1
    end = 10**x
    for left in range(start, end):
        s = str(left)
        if i % 2 == 0:
            pal = int(s + s[::-1])
        else:
            pal = int(s + s[-2::-1])
        if pal > N:
            break
        b = base_n(pal, A)
        if b != -1 and is_palindrome(b):
            ans += pal
print(ans)