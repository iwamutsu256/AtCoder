N = int(input())
A = list(map(int,input().split()))
dic = {}
for i in range(N):
    if A[i] in dic:
        print(dic[A[i]],end=" ")
        dic[A[i]] = i+1
    else:
        dic[A[i]] = i+1
        print(-1,end=" ")
print()