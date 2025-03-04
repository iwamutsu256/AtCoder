N,M = map(int,input().split())
H = [int(x) for x in input().split()]
First = True
for i in range(N):
    M -= H[i]
    if M < 0 and First == True:
        print(i)
        First = False
if First == True:
    print(N)