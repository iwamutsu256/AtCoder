s = list(input())
if len(s) != 8:
    print("No")
elif not ("A" <= s[0] <= "Z"):
    print("No")
elif "".join(s[1:7]).isdigit() == False:
    print("No")
elif not(100000 <= int("".join(s[1:7])) <= 999999):
    print("No")
elif not ("A" <= s[7] <= "Z"):
    print("No")
else:
    print("Yes")