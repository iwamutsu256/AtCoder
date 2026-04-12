S = list(input())
count = 0
i = 0
while 3+2*i <= len(S):
    for j in range(len(S)-2*i-3+1):
        if S[j]=="A" and S[j+i+1] == "B" and S[j+2*i+2] == "C":
            #print(j,j+i+1,j+2*i+2)
            count += 1
    i += 1
print(count)