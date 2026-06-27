S = list(input())
west = 0
for i in range(len(S)):
    if S[i] == "W":
        west += 1
if len(S) - west < west:
    print("West")
else:
    print("East")