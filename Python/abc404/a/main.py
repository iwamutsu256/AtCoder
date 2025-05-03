S = set(list(input()))
A = set([chr(i+97) for i in range(26)])
print(list(A-S)[0])