N = int(input())
H = [int(x) for x in input().split()]
for i in range(N-1):
    if H[0] < H[i+1]:
        print(i+2)
        break
else:
    print(-1)