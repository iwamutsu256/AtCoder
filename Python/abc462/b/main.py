N = int(input())
dct = dict()
for i in range(N):
    dct[i+1] = []

for i in range(N):
    A = list(map(int,input().split()))
    for j in range(1,A[0]+1):
        dct[A[j]].append(i+1)
for i in range(N):
    print(" ".join([str(len(dct[i+1]))]+list(map(str,dct[i+1]))))