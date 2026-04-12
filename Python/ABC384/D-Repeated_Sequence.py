N,S = map(int,input().split())
A = [int(x) for x in input().split()]
Sum = sum(A)
Sa = set()
Sb = 0
for i in range(N):
    Sb += A[i]
    Sa.add(Sb)
for i in range(N):
    Sb += A[i]
    Sa.add(Sb)
M = S % Sum
#print(Sa)
for x in Sa:
    if x - M in Sa:
        print("Yes")
        break
else:
    print("No")