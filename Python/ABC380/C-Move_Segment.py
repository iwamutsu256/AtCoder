N,K = map(int,input().split())
S = input()
count = 0
l = 1
j = N-1
for i in range(N):
    if i > 1 and int(S[i])-int(S[i-1]) == -1:
        count += 1
        if count == K-1:
            l = i
        if count == K:
            j = i-1
        #print(count)
    #print(S[i],end="")
for i in range(N):
    if l <= i and i <= j:
        print(S[j+l-i],end="")
    else:
        print(S[i],end="")
print()