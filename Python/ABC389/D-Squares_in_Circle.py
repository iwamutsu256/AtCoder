R = int(input())
K = [0]*1000000

for i in range(1,R):
    K[i] = int(((R**2-(-1*R-0.5+i)**2)**0.5+0.5)//1)
    #print((R**2-(-1*R-0.5+i)**2)**0.5+0.5)
#    while K[i]+1 <= (R**2-(-1*R-0.5+i)**2)**0.5:

ans = 0
for i in range(1,R):
    #print(K[i])
    ans += K[i]
print(4*ans+1)
