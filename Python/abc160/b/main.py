X = int(input())
A = 0
B = 0
while X >= 500:
    A += 1
    X -= 500
while X >= 5:
    B += 1
    X -= 5
print(A*1000+B*5)