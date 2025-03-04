def strings(S):
    if len(S) % 2 != 0:
        return False
    for i in range(len(S)//2):
        if S[2*i] != S[2*i+1]:
            return False
    for i in range(26):
        if S.count(chr(97+i)) != 0 and S.count(chr(97+i)) != 2:
            return False
    return True

S = input()
if strings(S):
    print("Yes")
else:
    print("No")