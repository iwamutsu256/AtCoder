a,b,c = map(int,input().split())

# A*n % B == C

# A*n - C == B*m
for i in range(b):
    if (a*i)%b == c:
        print("YES")
        break
else:
    print("NO")