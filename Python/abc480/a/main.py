s = list(input())
t = list(input())
if (s[0] in ("A","D") and t[1] in ("A","D")) or (s[1] in ("A","D") and t[0] in ("A","D")):
    print("No")
else:
    print("Yes")