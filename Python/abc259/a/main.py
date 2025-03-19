N,M,X,T,D = map(int,input().split())
first = T-D*X
if M <= X:
    print(first + D*M)
else:
    print(T)