def emptymasu(a,b):
    global count
    if 0 < a and a <= N and 0 < b and b <= N and (a , b) not in board:
        board.add((a,b))
        count += 1

def setmasu(a,b):
    emptymasu(a+2,b+1)
    emptymasu(a+1,b+2)
    emptymasu(a-1,b+2)
    emptymasu(a-2,b+1)
    emptymasu(a-2,b-1)
    emptymasu(a-1,b-2)
    emptymasu(a+1,b-2)
    emptymasu(a+2,b-1)
    emptymasu(a,b)

N,M = map(int,input().split())
board = set()
count = 0
for i in range(M):
    A,B = map(int,input().split())
    setmasu(A,B)
result = count
print(N**2-result)

