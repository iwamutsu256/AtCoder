T = int(input())
for _ in range(T):
    X1,Y1,R1,X2,Y2,R2 = map(int,input().split())
    dist = (X1-X2)**2 + (Y1-Y2)**2
    if dist <= (R1+R2)**2 and dist >= (R1-R2)**2:
        print("Yes")
    else:
        print("No")