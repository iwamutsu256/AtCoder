S = list(input())
ans = 0
for i in range(len(S)-1):
    for j in range(i+1,len(S)):
        num = 0
        if S[i] == S[j] and j-i > 1 and S[i] == "t":
            count = 0
            for k in range(i+1,j):
                if S[k] == S[i]:
                    count += 1
            num = count / (j-i-1)
        else:
            num = 0
        ans = max(ans, num)
print(ans)