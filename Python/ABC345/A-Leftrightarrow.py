S = input()
if S[0] == "<" and S[-1] == ">" and S.count("=") == len(S)-2:
    print("Yes")
else:
    print("No")