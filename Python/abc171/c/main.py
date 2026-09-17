n = int(input())
# n-=1
a = "abcdefghijklmnopqrstuvwxyz"
ans = ""
while n > 0:
    n-=1
    ans = a[n%26] + ans
    n //= 26
print(ans)

# 0~25
