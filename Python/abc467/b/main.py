n = int(input())
minus = 0
for _ in range(n):
    a,b,s = input().split()
    a = int(a)
    b = int(b)
    if s == "keep":
        minus += b-a
print(minus)