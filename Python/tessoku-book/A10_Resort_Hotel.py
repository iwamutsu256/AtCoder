N = int(input())
A = [int(x) for x in input().split()]
D = int(input())
Left = [0]*(len(A)+1)
Right = [0]*(len(A)+1)
for i in range(1,len(A)+1):
    Left[i] = max(Left[i-1],A[i-1])
    Right[-i] = max(Right[-i+1],A[-i])
for i in range(D):
    L,R = map(int,input().split())
    print(max(Left[L-1],Right[R+1]))
#print(Left,Right)