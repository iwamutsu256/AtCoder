N = int(input())
S = ""
for i in range(N):
    c,l = input().split()
    l = int(l)
    if len(S)+l <= 100:
        S += c*l
    else:
        print("Too Long")
        break
else:
    print(S)