N = int(input())
for i in range(10):
    exp = 2**(10-i-1)
    print((N//exp)%2,end="")
print()