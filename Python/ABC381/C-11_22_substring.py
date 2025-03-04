N = int(input())
S = input()
one_count = 0
two_count = 0
mx = 0
for i in range(N):
    if i > 0:
        if S[i] == "1":
            if S[i-1] != "2":
                one_count += 1
            else:
                two_count = 0
                one_count = 1
        elif S[i] == "2":
            if S[i-1] != "1":
                two_count += 1
            else:
                two_count = 0
                one_count = 0
        else:
            if S[i-1] != "1":
                two_count = 0
                one_count = 0
                mx = max(mx,min(one_count,two_count))
    else:
        if S[i] == "1":
            one_count += 1
print(mx)