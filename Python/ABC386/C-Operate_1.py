K = int(input())
S = input()
T = input()
if len(S) == len(T):
    count = 0
    for i in range(len(S)):
        if S[i] != T[i]:
            count += 1
    if count <= 1:
        print("Yes")
    else:
        print("No")
elif len(S) == len(T) + 1:
    count = 0
    for i in range(len(T)):
        if count == 0 and S[i] != T[i]:
            count += 1
        if count == 1 and S[i+1] != T[i]:
            count += 1
    if count <= 1:
        print("Yes")
    else:
        print("No")
elif len(S) == len(T) - 1:
    count = 0
    for i in range(len(S)):
        if count == 0 and S[i] != T[i]:
            count += 1
        if count == 1 and S[i] != T[i+1]:
            count += 1
    if count <= 1:
        print("Yes")
    else:
        print("No")
else:
    print("No")