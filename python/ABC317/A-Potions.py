N,H,X = map(int,input().split())
P = [int(x) for x in input().split()]
HP = True
i = 1
while HP:
    if X-H <= P[i-1]:
        HP = False
    else:
        i += 1
print(i)