S = list(map(int,list(input())))
count = 0
for i in range(len(S)-1):
    if S[i] - S[i+1] >= 0:
        count += S[i] - S[i+1]
    else:
        count += S[i] - S[i+1] + 10
count += len(S) + S[-1]
print(count)