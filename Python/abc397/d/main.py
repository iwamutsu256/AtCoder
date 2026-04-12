import math
N = int(input())
for i in range(1,int(math.pow(N,1/3))+1):
    a = math.pow(9*math.pow(i,4)-12*i*(math.pow(i,3)-N),1/2)
    if  a % 1 == 0:
        b = (-3*math.pow(i,2)+a)/(6*i)
        if b % 1 == 0 and b > 0:
            print(int(i+b),int(b))
            break
else:
    print(-1)