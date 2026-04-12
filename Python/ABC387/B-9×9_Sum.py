X = int(input())
P = []
for i in range(1,10):
    for j in range(1,10):
        P.append(i*j)
print(2025-X*P.count(X))