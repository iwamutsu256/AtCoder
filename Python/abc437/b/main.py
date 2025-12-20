H,W,N = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
H_list = [0 for _ in range(H)]
for i in range(N):
    num = int(input())
    for j in range(H):
        if num in A[j]:
            H_list[j] += 1
print(max(H_list))
