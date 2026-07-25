s = list(input())
# 奇数文字中心
ans = 0
for i in range(len(s)):
    state = 0
    plus = 0
    while state != 2 and i-plus >= 0 and i+plus < len(s):
        if state == 0:
            ans += 1
            if s[i+plus] != s[i-plus]:
                state += 1
        elif state == 1:
            if s[i+plus] == s[i-plus]:
                ans += 1
            else:
                state += 1
        else:
            pass
        plus += 1
# 偶数文字中心
for i in range(len(s)-1):
    state = 0
    plus = 0
    while state != 2 and i-plus >= 0 and i+plus+1 < len(s):
        if state == 0:
            ans += 1
            if s[i+plus+1] != s[i-plus]:
                state += 1
        elif state == 1:
            if s[i+plus+1] == s[i-plus]:
                ans += 1
            else:
                state += 1
        else:
            pass
        plus += 1
print(ans)