S = list(input())
ans = 0
len_count = 0
prev_char = "x"
for i in range(len(S)):
    if S[i] == prev_char:
        len_count = 0
    len_count += 1
    ans += len_count
    ans = ans % 998244353
    prev_char = S[i]
print(ans)