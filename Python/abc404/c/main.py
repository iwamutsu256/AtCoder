N,M = map(int,input().split())
dict = dict()
for i in range(M):
    A,B = map(int,input().split())
    if A in dict:
        dict[A].append(B)
    else:
        dict[A] = [B]
    if B in dict:
        dict[B].append(A)
    else:
        dict[B] = [A]
if N != M or len(dict) != N:
    print("No")
else:
    before = None
    current = 1
    for i in range(N):
        if len(dict[current]) != 2:
            print("No")
            break
        else:
            if before != None:
                dict[current].remove(before)
            before = current
            current = dict[current][0]
    else:
        print("Yes")
