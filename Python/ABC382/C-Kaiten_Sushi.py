def search(num,left,right):
    if right == left:
        return C[right]+1
    if A[C[right]] > num:
        return -1
    else:
        center = (right + left)//2
        if A[C[center]] > num:
            return search(num,center+1,right)
        elif A[C[center]] == num:
            return C[center]+1
        else:
            return search(num,left,center)

N,M = map(int,input().split())
A = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
C = []
for i in range(N):
    if i == 0:
        min = A[0]
        C.append(0)
    elif A[i] < min:
        min = A[i]
        C.append(i)
for i in range(M):
    print(search(B[i],0,len(C)-1))