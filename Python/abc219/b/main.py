S1 = input()
S2 = input()
S3 = input()
T = list(input())
for i in range(len(T)):
    if T[i] == "1":
        T[i] = S1
    elif T[i] == "2":
        T[i] = S2
    else:
        T[i] = S3
print("".join(T))