N = int(input())
X = 0
Y = 0
for i in range(N):
    P = list(map(int,input().split()))
    X += P[0]
    Y += P[1]
if X>Y:
    print("Takahashi")
elif X<Y:
    print("Aoki")
else:
    print("Draw")