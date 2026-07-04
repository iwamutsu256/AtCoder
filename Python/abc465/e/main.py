s = input()
# 3の倍数 = 各桁の和が3の倍数
# 桁DP 3の倍数かつ3を含まず3種類でない
# 3を含むか、使った数字の種類、3の倍数か、現在の桁

# ここから解説を読んで実装
MODINT = 998244353

# 以下を持てばいい
# 使う数字の集合b (10文字なので、2**10=1024通り)
# 3で割ったあまりm (0~2の3通り)
# Nの冒頭i桁と比べて小さいか等しいかl (真偽値の2通り)(等しければ0)
# 
# DPとして、i桁目 (500桁なので、501通り)
# dp[i][b][m][l]
dp = [[[[0 for _ in range(2)] for _ in range(3)] for _ in range(2**10)] for _ in range(501)]

dp[0][0][0][0] = 1

for i in range(len(s)):
    for b in range(2**10):
        for m in range(3):
            for d in range(10):
                new_b = 0 if b==0 and d==0 else b|(2**d)
                new_m = (m*10 + d) % 3
                if d == int(s[i]):
                    dp[i+1][new_b][new_m][0] += dp[i][b][m][0]
                    dp[i+1][new_b][new_m][0] %= MODINT
                elif d < int(s[i]):
                    dp[i+1][new_b][new_m][1] += dp[i][b][m][0]
                dp[i+1][new_b][new_m][1] += dp[i][b][m][1]
                dp[i+1][new_b][new_m][1] %= MODINT

# dp内の要素について、いくつの制約を満たしているかカウントし、ひとつだったら答えに加算
ans = 0
for b in range(2**10):
    for m in range(3):
        for l in range(2):
            count = 0
            # 文字の種類の数
            if bin(b).count('1') == 3:
                count += 1
            # 3を含むかどうか
            if (2**3)&b == 2**3:
                count += 1
            # 3の倍数かどうか
            # ここですべての桁が0だった場合を取り除かなければいけない
            if m == 0 and b != 0:
                count += 1
            if count == 1:
                ans += dp[len(s)][b][m][l]
                ans %= MODINT
print(ans)