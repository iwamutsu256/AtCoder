N,S,K = map(int,input().split())
Sum = 0
for i in range(N):
    P,Q = map(int,input().split())
    Sum += P*Q
if Sum >=S:
    print(Sum)
else:
    print(Sum+K)