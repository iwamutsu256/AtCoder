N = int(input())
A = [None for _ in range(N)]
for i in range(N):
    if N % 2 == 0:
        if i == N // 2 or i == N // 2 - 1:
            A[i] = "="
        else:
            A[i] = "-"
    else:
        if i == N // 2:
            A[i] = "="
        else:
            A[i] = "-"
print("".join(A))