N,M = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
A.sort()
B.sort()
count = 0
while A and B:
    neta = B.pop()
    syari = A.pop()
    if neta > syari*2:
        while neta > syari*2:
            if len(B) == 0:
                break
            neta = B.pop()
    if neta > syari*2:
        break
    count += 1
print(count)