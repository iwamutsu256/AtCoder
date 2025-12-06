N = int(input())
A = list(map(int,input().split()))
maxi = 0
count = 0
for i in range(len(A)):
    if i == 0:
        maxi = A[i]
        count = 1
    else:
        if i == maxi:
            break
        else:
            if i + A[i] > maxi:
                maxi = i+A[i]
            count += 1
print(count)