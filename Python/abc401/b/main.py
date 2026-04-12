N = int(input())
Status = False
count = 0
for i in range(N):
    S = input()
    if S == "login":
        Status = True
    elif S == "logout":
        Status = False
    elif Status == False and S == "private":
        count += 1
print(count)