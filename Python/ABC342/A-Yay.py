S = input()
if S.count(S[0]) == 1:
    print(1)
else:
    for i in range(len(S)-1):
        if S[i+1] != S[0]:
            print(i+2)
