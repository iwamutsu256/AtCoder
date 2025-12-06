N = int(input())
A = [0] + list(map(int,input().split()))
sumA = [0 for _ in range(len(A))]
for i in range(len(A)):
    if i == 0:
        sumA[i] = A[i]
    else:
        sumA[i] = sumA[i-1] + A[i]
count = 0
# print(sumA)
for i in range(2,N+1):
    for j in range(1,i):
        # print(j,i)
        flag = True
        sumB = sumA[i]-sumA[j-1]
        for k in range(j,i+1):
            if sumB % A[k] == 0:
                flag = False
                break
        if flag:
            count += 1
print(count)