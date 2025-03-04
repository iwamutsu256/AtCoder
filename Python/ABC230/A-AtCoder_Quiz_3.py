N = int(input())
if N >= 42:
    N += 1
if N < 10:
    N = "AGC00" + str(N)
else:
    N = "AGC0" + str(N)
print(N)