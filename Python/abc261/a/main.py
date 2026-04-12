L1,R1,L2,R2 = map(int,input().split())
X = [1 if L1 <= i <= R1 else 0 for i in range(101)]
Y = [1 if L2 <= i <= R2 else 0 for i in range(101)]
print(sum([X[i]*Y[i] for i in range(101)])-1 if sum([X[i]*Y[i] for i in range(101)]) > 0 else 0)