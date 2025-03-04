N = int(input())
user = set()
for i in range(N):
    S = input()
    if not S in user:
        user.add(S)
        print(i+1)
