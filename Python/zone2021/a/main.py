S = input()
count = 0
if len(S) >= 4:
    for i in range(len(S)-3):
        if S[i:i+4] == "ZONe":
            count += 1
print(count)