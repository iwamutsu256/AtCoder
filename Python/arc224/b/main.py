from math import isqrt
t = int(input())
for _ in range(t):
    n = int(input())
    ans = 0
    rootn = isqrt(n)
    # print(f"rootn:{rootn}")
    ans += rootn*(rootn-1)*2
    nokori = n - (rootn**2)
    if nokori > rootn:
        ans += (nokori-1)*2
    elif nokori == 0:
        pass
    else:
        ans += nokori*2 - 1
    print(ans)
