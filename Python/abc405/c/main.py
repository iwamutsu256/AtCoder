N = int(input())
A = list(map(int,input().split()))
suma = sum(A)
B = 0
for i in A:
    B += i**2
print((suma**2-B)//2)